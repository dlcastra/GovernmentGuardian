from django.middleware.csrf import get_token
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from app.models import Lawyer, Client, Feedback, Case


def get_user_type(request):
    if request.user.is_authenticated:
        if Lawyer.objects.filter(user=request.user).exists():
            return True
        elif Client.objects.filter(user=request.user).exists():
            return False
        else:
            return render(request, "profiles/not_authenticated.html")

    else:
        return render(request, "profiles/not_authenticated.html")


def redirect_based_on_user_type(request, redirect_if_lawyer, redirect_if_client):
    user_type = get_user_type(request)
    if user_type:
        return redirect(redirect_if_lawyer)
    else:
        return redirect(redirect_if_client)


def edit_method(request, form_instance, post_form_instance, render_template, redirect_url):
    if request.method == "GET":
        form = form_instance
        return render(request, render_template, {"form": form})

    form = post_form_instance
    if form.is_valid():
        instance = form.save(commit=False)
        if "image" in request.FILES:
            instance.image = request.FILES["image"]

        instance.save()
        form.save()
        return redirect(redirect_url)


def data_handler(request, lawyer_id):
    feedback = Feedback.objects.filter(lawyer_id=lawyer_id).all()
    client_id = Client.objects.get(user=request.user).id
    has_case_with_lawyer = Case.objects.filter(client_id=client_id, lawyer_id=lawyer_id).exists()
    feedback_html = render_to_string("ordering/feedback_section.html",
                                     {"feedback": feedback, "has_case_with_lawyer": has_case_with_lawyer,
                                      "csrf_token": get_token(request), "client_id": client_id})
    csrf_token = get_token(request)
    return {"feedback_html": feedback_html, "client_id": client_id,
            "has_case_with_lawyer": has_case_with_lawyer, "csrf_token": csrf_token}
