from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import ClientForm, LawyerForm
from app.models import Lawyer, Client
from users.forms import UserCreationFormWithEmail

""" --- SIGN UP AND SIGN IN --- """

oauth = OAuth()


def send_activation_email(request, user: User):
    user_signed = Signer().sign(user.id)
    signed_url = request.build_absolute_uri(f"/activate/{user_signed}")
    send_mail(
        subject="Registration successfully completed",
        message=("Click here to activate your account: " + signed_url),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def register_view(request):
    if request.method == "GET":
        form = UserCreationFormWithEmail()
        return render(request, "registration/register.html", {"form": form})

    form = UserCreationFormWithEmail(request.POST)
    if form.is_valid():
        form.instance.is_active = False
        form.save()
        send_activation_email(request, form.instance)
        return redirect("login_view")

    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user
        lawyer = Lawyer.objects.filter(user=user)
        client = Client.objects.filter(user=user)
        if lawyer.exists() or client.exists():
            return "/get-list/"
        else:
            return "/select-role/"


def activate(request, user_signed):
    try:
        user_id = Signer().unsign(user_signed)
    except BadSignature:
        return redirect("login_view")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login_view")
    user.is_active = True
    user.save()
    return redirect("login_view")


oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    user_email = token
    user, created = User.objects.get_or_create(email=user_email)
    user.save()

    return redirect(request.build_absolute_uri(reverse("roles")))


def login(request):
    return oauth.auth0.authorize_redirect(request, request.build_absolute_uri(reverse("callback")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


""" --- CLIENT OR LAWYER ---"""


def select_role(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role == "client":
            return redirect("create_client")
        elif role == "lawyer":
            return redirect("create_lawyer")

    return render(request, "roles/select_role.html")


def client_registration(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect("list")
    else:
        form = ClientForm()
    return render(request, "roles/client_registration.html", {"form": form})


def lawyer_registration(request):
    if request.method == "POST":
        form = LawyerForm(request.POST)
        if form.is_valid():
            lawyer = form.save(commit=False)
            lawyer.user = request.user
            lawyer.save()
            return redirect("list")
    else:
        form = LawyerForm()
    return render(request, "roles/lawyer_registration.html", {"form": form})
