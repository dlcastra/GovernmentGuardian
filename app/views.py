from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from app.forms import ClientForm, ClientCaseForm, EditLawyerForm, LawyerCaseForm
from app.helpers import redirect_based_on_user_type, edit_method
from app.models import Lawyer, Client, Case, Feedback

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
    get_instance = EditLawyerForm(instance=lawyer)
    post_instance = EditLawyerForm(request.POST, instance=lawyer)

    return edit_method(request, lawyer, get_instance, post_instance, "profiles/edit_profile.html", "lawyer_profile")


def lawyer_active_cases(request):
    user = request.user
    lawyer = get_object_or_404(Lawyer, user=user)
    cases = Case.objects.filter(lawyer=lawyer, is_active=True)

    if "close_case" in request.GET:
        case_id = request.GET.get("close_case")
        return redirect("close_case", case_id=case_id)

    return render(request, "profiles/lawyer/cases.html", {"cases": cases})


def close_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    instance = LawyerCaseForm(instance=case)
    post_instance = LawyerCaseForm(request.POST, instance=case)

    return edit_method(request, case, instance, post_instance, "profiles/lawyer/close_case.html", "lawyer_active_cases")


""" --- FUNCTIONS FOR CLIENT ---"""


def client_profile(request):
    user = request.user
    client = Client.objects.get(user=user)
    case = Case.objects.filter(client=client, is_active=True)
    context = {"client": client, "case": case}
    return render(request, "profiles/client/client_profile.html", context)


def edit_client_profile(request):
    client = get_object_or_404(Client, user=request.user)
    get_instance = ClientForm(instance=client)
    post_instance = ClientForm(request.POST, instance=client)

    return edit_method(request, client, get_instance, post_instance, "profiles/edit_profile.html", "client_profile")


def retain_lawyer(request, lawyer_id):
    client = Client.objects.get(user=request.user)
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
    case = Case.objects.filter(client=client, is_active=True)
    feedback = Feedback.objects.filter(lawyer=lawyer)
    feedback_handler(request, lawyer, client)
    csrf_token = get_token(request)
    feedback_context = {"lawyer": lawyer, "feedback": feedback,
                        "case": Case.objects.filter(lawyer=lawyer,
                                                    is_active=False,
                                                    case_closed_successfully=True), "csrf_toke": csrf_token}
    feedback_html = render_to_string("ordering/feedback_section.html", context=feedback_context)
    get_info_context = {"lawyer": lawyer, "feedback": feedback, "case": Case.objects.filter(lawyer=lawyer),
                        "client": client, }
    if "get_info" in request.GET:
        get_info_context["feedback_html"] = feedback_html
        return render(request, "ordering/lawyer_info.html", context=get_info_context)

    elif "retain" in request.GET and case.exists():
        return redirect("lawyer_already_taken")

    elif "retain" in request.GET:
        return redirect("create_case", lawyer_id)
    if request.method == "POST":
        return JsonResponse(feedback_html, safe=False)

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


def profile(request):
    return redirect_based_on_user_type(request, "lawyer_profile", "client_profile")


def navigation_user_info(request):
    return redirect_based_on_user_type(request, "lawyer_active_cases", "list")


""" --- CUSTOM ERRORS --- """


def custom_404(request, exception=None):
    return render(request, "errors/404.html")


""" --- FEEDBACK --- """


def feedback_handler(request, lawyer, client):
    case = Case.objects.filter(lawyer=lawyer, client=client)
    content = request.POST.get("feedback")
    if request.method == "POST":
        Feedback.objects.create(client=case.get.client, lawyer=case.get.lawyer, case=case, text=content, title=case.article)
