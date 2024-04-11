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
    total_cases = lawyer.successful_cases + lawyer.unsuccessful_cases
    success_percentage = (lawyer.successful_cases / total_cases) * 100
    failure_percentage = (lawyer.unsuccessful_cases / total_cases) * 100
    context = {
        'lawyer': lawyer,
        'success_percentage': success_percentage,
        'failure_percentage': failure_percentage,
    }
    return render(request, "profiles/lawyer/lawyer_profile.html", context)


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


""" --- COMMON FUNCTIONS --- """


def profile(request):
    if request.user.is_authenticated:

        if Client.objects.filter(user=request.user).exists():
            return redirect("client_profile")
        elif Lawyer.objects.filter(user=request.user).exists():
            return redirect("lawyer_profile")
        else:
            return render(request, "profiles/not_authenticated.html")

    else:
        return render(request, "profiles/not_authenticated.html")
