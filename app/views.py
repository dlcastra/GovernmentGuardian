from django.shortcuts import render, redirect, get_object_or_404

from app.forms import ClientForm, ClientCaseForm, EditLawyerForm
from app.models import Lawyer, Client, Case

""" --- HOME PAGE --- """


def greeting_page(request):
    return render(request, "greeting_page.html")


def lawyers_list(request):
    lawyers = Lawyer.objects.all()
    return render(request, "lawyers_list.html", {"lawyers": lawyers})


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
        form = EditLawyerForm(instance=lawyer)
        return render(request, "profiles/edit_profile.html", {"form": form})

    if request.method == "POST":
        form = EditLawyerForm(request.POST, instance=lawyer)
        if form.is_valid():
            form.save()
            return redirect("lawyer_profile")

    return render(request, "profiles/edit_profile.html", {"form": lawyer})


def lawyer_active_cases(request):
    user = request.user
    lawyer = get_object_or_404(Lawyer, user=user)
    cases = Case.objects.filter(lawyer=lawyer, is_active=True)

    return render(request, "profiles/lawyer/cases.html", {"cases": cases})


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


def retain_lawyer(request, lawyer_id):
    client = Client.objects.get(user=request.user)
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
    case = Case.objects.filter(client=client, is_active=True)

    if "get_info" in request.GET:
        return render(request, "ordering/lawyer_info.html", {"lawyer": lawyer})

    elif "retain" in request.GET and case.exists():
        return redirect("lawyer_already_taken")

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


def lawyer_already_taken(request):
    return render(request, "ordering/lawyer_already_taken.html")


""" --- COMMON FUNCTIONS --- """


def who_is_user(request):
    if request.user.is_authenticated:
        if Lawyer.objects.filter(user=request.user).exists():
            return True

        elif Client.objects.filter(user=request.user).exists():
            return False

        else:
            return render(request, "profiles/not_authenticated.html")

    else:
        return render(request, "profiles/not_authenticated.html")


def profile(request):
    user_type = who_is_user(request)
    if user_type:
        return redirect("lawyer_profile")
    else:
        return redirect("client_profile")


def navigation_user_info(request):
    user_type = who_is_user(request)
    if user_type:
        return redirect("lawyer_active_cases")
    else:
        return redirect("list")


""" --- CUSTOM ERRORS --- """


def custom_404(request, exception=None):
    return render(request, "errors/404.html")
