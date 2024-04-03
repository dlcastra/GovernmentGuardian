from django.contrib.auth.views import LoginView
from django.urls import path

from users import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("google-login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("activate/<user_signed>", views.activate, name="activate"),
    path("select-role/", views.select_role, name="roles"),
    path("create-client/", views.client_registration, name="create_client"),
    path("create-lawyer/", views.lawyer_registration, name="create_lawyer")
]
