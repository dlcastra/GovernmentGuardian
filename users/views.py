from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from celery import shared_task
from app.forms import ClientForm, LawyerForm
from app.mixins import CreateObjectMixin
from app.models import Lawyer, Client
from users.forms import UserCreationFormWithEmail

""" --- SIGN UP AND SIGN IN --- """

oauth = OAuth()


@shared_task
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
            return "/profile/"
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
    user_email = request.session["user"]["userinfo"]["email"]
    username = request.session["user"]["userinfo"]["nickname"]

    try:
        user = User.objects.get(username=username)
        login(request, user)
        return redirect(reverse("profile"))
    except User.DoesNotExist:
        pass
    except IntegrityError:
        User.objects.get(username=username)

    user = User.objects.create_user(username=username, email=user_email, is_active=True)
    user.save()
    login(request, user)

    return redirect(reverse("roles"))


def auth0_login(request):
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


class CreateClientView(CreateObjectMixin, View):
    template_name = "roles/client_registration.html"
    form_instance_class = ClientForm
    success_url = "list"


class CreateLawyerView(CreateObjectMixin, View):
    template_name = "roles/client_registration.html"
    form_instance_class = LawyerForm
    success_url = "profile"
