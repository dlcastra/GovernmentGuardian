from django.shortcuts import render, redirect

from app.forms import LawyerForm
from app.models import Lawyer


def register(request):
    ...


def index(request):
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
