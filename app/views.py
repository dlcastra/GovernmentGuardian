from django.shortcuts import render, redirect, get_object_or_404

from app.forms import LawyerForm, ClientForm
from app.models import Lawyer, Client

""" --- HOME PAGE --- """


def index(request):
    return render(request, "wpage.html")


def lawyers_list(request):
    lawyers = Lawyer.objects.all()
    return render(request, "index.html", {"lawyers": lawyers})


""" --- FUNCTIONS FOR LAWYER --- """


def lawyer_profile(request):
    user = request.user
    lawyer = Lawyer.objects.get(user=user)
    return render(request, "profiles/lawyer/lawyer_profile.html", {"lawyer": lawyer})


def edit_lawyer_profile(request):
    lawyer = get_object_or_404(Lawyer, user=request.user)
    if request.method == "GET":
        form = LawyerForm(instance=lawyer)
        return render(request, "profiles/edit_profile.html", {"form": form})

    if request.method == "POST":
        form = LawyerForm(request.POST, instance=lawyer)
        if form.is_valid():
            form.save()
            return redirect("lawyer_profile")

    return render(request, "profiles/edit_profile.html", {"form": lawyer})


""" --- FUNCTIONS FOR CLIENT ---"""


def client_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    return render(request, "profiles/client/client_profile.html", {"client": client})


def edit_client_profile(request):
    client = get_object_or_404(Client, user=request.user)
    if request.method == "GET":
        form = ClientForm(instance=client)
        return render(request, "profiles/edit_profile.html", {"form": form})

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client_profile")

    return render(request, "profiles/edit_profile.html", {"form": client})
