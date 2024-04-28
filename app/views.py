from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from app.forms import ClientForm, ClientCaseForm, EditLawyerForm, LawyerCaseForm
from app.helpers import redirect_based_on_user_type, get_feedback_data
from app.mixins import EditObjectMixin
from app.models import Lawyer, Client, Case, Feedback

""" --- HOME PAGE --- """


class GreetingPageView(TemplateView):
    template_name = "greeting_page.html"


""" --- FUNCTIONS FOR LAWYER --- """


class LawyerProfileView(View):
    template_name = "profiles/lawyer/lawyer_profile.html"

    @staticmethod
    def get_context_data(request):
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
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        template = self.template_name
        return render(request, template, context)


class EditLawyerProfileView(EditObjectMixin, View):
    form_instance_class = EditLawyerForm
    success_url = "lawyer_profile"

    def get_object(self):
        return get_object_or_404(Lawyer, user=self.request.user)


class LawyerActiveCasesView(View):
    template_name = "profiles/lawyer/cases.html"

    @staticmethod
    def get_context_data(request):
        user = request.user
        lawyer = get_object_or_404(Lawyer, user=user)
        cases = Case.objects.filter(lawyer=lawyer, is_active=True)

        return cases

    def get(self, request, *args, **kwargs):
        template = self.template_name
        context = self.get_context_data(request)

        if "close_case" in request.GET:
            case_id = request.GET.get("close_case")
            return redirect("close_case", case_id=case_id)

        return render(request, template, {"cases": context})


class CloseCaseView(EditObjectMixin, View):
    template_name = "profiles/lawyer/close_case.html"
    form_instance_class = LawyerCaseForm
    success_url = "lawyer_active_cases"

    def get_object(self):
        return get_object_or_404(Case, pk=self.kwargs["case_id"])

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        lawyer = instance.lawyer
        form = self.form_instance_class(request.POST)

        if form.is_valid():
            instance.is_active = False
            if request.POST.get("case_closed_successfully"):
                lawyer.successful_cases += 1
            else:
                lawyer.unsuccessful_cases += 1
            form.save(commit=False)
            instance.save()
            lawyer.save()
            return redirect(self.success_url)

        return HttpResponse(form.errors)


""" --- FUNCTIONS FOR CLIENT ---"""


class ClientProfileView(View):
    template_name = "profiles/client/client_profile.html"

    @staticmethod
    def get_context_data(request):
        user = request.user
        client = Client.objects.get(user=user)
        case = Case.objects.filter(client=client, is_active=True)
        context = {"client": client, "case": case}

        return context

    def get(self, request, *args, **kwargs):
        template = self.template_name
        context = self.get_context_data(request)
        return render(request, template, context)


class EditClientProfileView(EditObjectMixin, View):
    form_instance_class = ClientForm
    success_url = "client_profile"

    def get_object(self):
        return get_object_or_404(Client, user=self.request.user)


class GetLawyerList(TemplateView):
    template_name = "lawyers_list.html"

    def get(self, request, *args, **kwargs):
        template = self.template_name
        lawyers = Lawyer.objects.all()
        return render(request, template, {"lawyers": lawyers})


def retain_lawyer(request, lawyer_id):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return HttpResponse("You are not a registered client.")
    case = Case.objects.filter(client=client, is_active=True)
    lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
    has_case_with_lawyer = Case.objects.filter(client=client, lawyer=lawyer).exists()

    feedback = Feedback.objects.filter(lawyer=lawyer).all()
    feedback_context = get_feedback_data(request, lawyer, has_case_with_lawyer, feedback)
    feedback_html = render_to_string("ordering/feedback_section.html", context=feedback_context)
    get_info_context = {
        "lawyer": lawyer,
        "feedback": feedback,
        "case": Case.objects.filter(lawyer=lawyer),
        "client": client,
        "csrf_token": get_token(request),
        "has_case_with_lawyer": has_case_with_lawyer,
        "feedback_html": feedback_html,
    }

    if "get_info" in request.GET:
        return render(request, "ordering/lawyer_info.html", context=get_info_context)
    elif "retain" in request.GET and case.exists():
        return redirect("lawyer_already_taken")
    elif "retain" in request.GET:
        return redirect("create_case", lawyer_id)
    return render(request, "ordering/lawyer_info.html", {"lawyer": lawyer})


class CreateCaseView(View):
    template_name = "ordering/case_form.html"
    success_url = "client_profile"

    def get_context_data(self, request):
        user = request.user
        client = Client.objects.get(user=user)
        lawyer = get_object_or_404(Lawyer, pk=self.kwargs["lawyer_id"])
        context = {"lawyer": lawyer, "client": client}

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        form = ClientCaseForm(initial=context)
        template = self.template_name

        return render(request, template, {"form": form})

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        lawyer = context["lawyer"]

        form = ClientCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.lawyer = lawyer
            case.save()
            return redirect(self.success_url)


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


@require_POST
def feedback_handler(request, lawyer, client):
    has_case_with_lawyer = Case.objects.filter(client_id=client, lawyer_id=lawyer).exists()
    feedback = Feedback.objects.filter(lawyer_id=lawyer)
    feedback_context = get_feedback_data(request, lawyer, has_case_with_lawyer, feedback)
    feedback_html = render_to_string("ordering/feedback_section.html", context=feedback_context)
    case = Case.objects.filter(lawyer_id=lawyer, client_id=client).first()
    if case:
        content = request.POST.get("feedback")
        Feedback.objects.create(client_id=client, lawyer_id=lawyer, case=case, text=content, title=case.article)
        return JsonResponse({"feedback_html": feedback_html})

    else:
        pass


@require_POST
def remove_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.delete()
    except Feedback.DoesNotExist:
        return JsonResponse({"error": "Feedback does not exist"}, status=404)
    return HttpResponse(status=204)
