from django.shortcuts import render, redirect
from django.views.generic import DetailView

from app.forms import LawyerForm, ClientForm
from app.models import Lawyer, Client

""" --- HOME PAGE --- """


def index(request):
    return render(request, "wpage.html")


def lawyers_list(request):
    lawyers = Lawyer.objects.all()
    return render(request, "index.html", {"lawyers": lawyers})


""" --- FUNCTIONS FOR LAWYER --- """


class LawyerProfile(DetailView):
    model = Lawyer
    template_name = "profiles/lawyer/lawyer_profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        lawyer = Lawyer.objects.get(user=user)
        return render(request, self.template_name, {"lawyer": lawyer})

    def post(self, request, *args, **kwargs):
        user = request.user
        lawyer = Lawyer.objects.get(user=user)
        form = LawyerForm(request.POST, instance=lawyer)

        if "edit" in request.POST:
            if form.is_valid():
                form.save()
                return redirect("lawyer_profile")

        return render(request, "profiles/lawyer/edit_profile.html", {"lawyer": form})


""" --- FUNCTIONS FOR CLIENT ---"""


class ClientProfile(DetailView):
    model = Client
    template_name = "profiles/client/client_profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        client = Client.objects.get(user=user)
        return render(request, self.template_name, {"client": client})

    def post(self, request, *args, **kwargs):
        user = request.user
        client = Client.objects.get(user=user)
        form = ClientForm(request.POST, instance=client)

        if "edit" in request.POST:
            if form.is_valid():
                form.save()
                return redirect("client_profile")

        return render(request, "profiles/client/edit_profile.html", {"client": form})
