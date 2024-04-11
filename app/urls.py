from django.conf.urls.static import static
from django.urls import path

from app import views
from core import settings

urlpatterns = [
    # Main pages
    path("", views.index, name="index"),
    path("get-list/", views.lawyers_list, name="list"),
    # Profile views
    path("profile/", views.profile, name="profile"),
    path("lawyer-profile/", views.lawyer_profile, name="lawyer_profile"),
    path("client-profile/", views.client_profile, name="client_profile"),
    path("edit-lawyer-profile/", views.edit_lawyer_profile, name="edit_lawyer"),
    path("edit-client-profile/", views.edit_client_profile, name="edit_client"),
    # Ordering
    path("get-lawyer-info/<int:lawyer_id>", views.retain_lawyer, name="lawyer_info"),
    path("create-case/<int:lawyer_id>", views.create_case, name="create_case"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
