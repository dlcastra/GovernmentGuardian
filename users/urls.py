from django.conf.urls.static import static
from django.urls import path

from core import settings
from users import views
from users.views import CreateClientView, CreateLawyerView

urlpatterns = [
    # registration and login
    path("register/", views.register_view, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login_view"),
    path("google-login", views.auth0_login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("activate/<user_signed>", views.activate, name="activate"),
    # User model creation
    path("select-role/", views.select_role, name="roles"),
    path("create-client/", CreateClientView.as_view(), name="create_client"),
    path("create-lawyer/", CreateLawyerView.as_view(), name="create_lawyer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
