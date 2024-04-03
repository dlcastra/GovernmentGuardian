from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import LawyerForm
from app.models import Lawyer

""" --- SIGN UP AND SIGN IN --- """

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):
    return render(request, "wpage.html")


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("list")))


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


""" --- CRUD FOR LAWYER --- """


def lawyers_list(request):
    lawyers = Lawyer.objects.all()
    return render(request, "index.html", {"lawyers": lawyers})


def add_lawyer(request):
    if request.method == "GET":
        form = LawyerForm()
        return render(request, "add_lawyer.html", {"form": form})

    form = LawyerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("index")

    return render(request, "add_lawyer.html", {"form": form})


""" --- CRUD FOR CLIENT ---"""
