from django.shortcuts import render, redirect, get_object_or_404

from app.forms import LawyerForm, ClientForm, ClientCaseForm
from app.models import Lawyer, Client, Case

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
        "lawyer": lawyer,
        "success_percentage": success_percentage,
        "failure_percentage": failure_percentage,
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


def retain_lawyer(request, lawyer_id):
    client = Client.objects.get(user=request.user)
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
    case = Case.objects.filter(client=client, is_active=True)

    if "get_info" in request.GET:
        return render(request, "ordering/lawyer_info.html", {"lawyer": lawyer})

    elif "retain" in request.GET and case.exists():
        return redirect("index")

    elif "retain" in request.GET:
        return redirect("create_case", lawyer_id)

    return render(request, "ordering/lawyer_info.html", {"lawyer": lawyer})


def create_case(request, lawyer_id):
    user = request.user
    client = Client.objects.get(user=user)
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
    if request.method == "GET":
        form = ClientCaseForm(initial={"lawyer": lawyer, "client": client})
        return render(request, "ordering/case_form.html", {"form": form})

    form = ClientCaseForm(request.POST)
    if form.is_valid():
        case = form.save(commit=False)
        case.lawyer = lawyer
        case.save()
        return redirect("client_profile")

    return render(request, "ordering/case_form.html", {"form": form})


""" --- FUNCTIONS FOR CLIENT ---"""


def client_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    case = Case.objects.filter(client=client, is_active=True)
    context = {"client": client, "case": case}
    return render(request, "profiles/client/client_profile.html", context)


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
