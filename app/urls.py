from django.conf.urls.static import static
from django.urls import path

from app import views, helpers
from core import settings

urlpatterns = [
    # Main pages
    path("", views.greeting_page, name="index"),
    path("get-list/", views.lawyers_list, name="list"),
    # Profile views
    path("lawyer-profile/", views.lawyer_profile, name="lawyer_profile"),
    path("client-profile/", views.client_profile, name="client_profile"),
    path("edit-lawyer-profile/", views.edit_lawyer_profile, name="edit_lawyer"),
    path("edit-client-profile/", views.edit_client_profile, name="edit_client"),
    path("active-cases/", views.lawyer_active_cases, name="lawyer_active_cases"),
    path("close-case/<int:case_id>", views.close_case, name="close_case"),
    # Navigation panel
    path("who-is-user/", helpers.get_user_type, name="who_is_user"),
    path("profile/", views.profile, name="profile"),
    path("navigation/", views.navigation_user_info, name="navigation"),
    # Ordering
    path("get-lawyer-info/<int:lawyer_id>", views.retain_lawyer, name="lawyer_info"),
    path("create-case/<int:lawyer_id>", views.create_case, name="create_case"),
    path("lawyer-already-taken/", views.lawyer_already_taken, name="lawyer_already_taken"),
    # Feedback
    path("post-feedback/<int:lawyer>/<int:client>/", views.feedback_handler, name="post_feedback"),
    path("remove-feedback/<int:feedback_id>/", views.remove_feedback, name="remove_feedback"),
    # Errors
    path("404/", views.custom_404, name="custom_404"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
