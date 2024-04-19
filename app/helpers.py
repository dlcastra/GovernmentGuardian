from django.shortcuts import redirect, render

from app.models import Lawyer, Client


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


def edit_method(request, obj, form_instance, post_form_instance, render_template, redirect_url):
    if request.method == "GET":
        form = form_instance
        return render(request, render_template, {"form": form})

    if request.method == "POST":
        form = post_form_instance
        if form.is_valid():
            form.save()
            return redirect(redirect_url)

    return render(request, render_template, {"form": obj})