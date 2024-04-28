from django.conf.urls.static import static
from django.urls import path

from app import views, helpers
from core import settings
from app.views import (
    GreetingPageView,
    LawyerProfileView,
    EditLawyerProfileView,
    LawyerActiveCasesView,
    CloseCaseView,
    ClientProfileView,
    EditClientProfileView,
    GetLawyerList,
    CreateCaseView,
)

urlpatterns = [
    # Main pages
    path("", GreetingPageView.as_view(), name="index"),
    path("get-list/", GetLawyerList.as_view(), name="list"),
    # Profile views
    path("lawyer-profile/", LawyerProfileView.as_view(), name="lawyer_profile"),
    path("client-profile/", ClientProfileView.as_view(), name="client_profile"),
    path("edit-lawyer-profile/", EditLawyerProfileView.as_view(), name="edit_lawyer"),
    path("edit-client-profile/", EditClientProfileView.as_view(), name="edit_client"),
    path("active-cases/", LawyerActiveCasesView.as_view(), name="lawyer_active_cases"),
    path("close-case/<int:case_id>", CloseCaseView.as_view(), name="close_case"),
    # Navigation panel
    path("who-is-user/", helpers.get_user_type, name="who_is_user"),
    path("profile/", views.profile, name="profile"),
    path("navigation/", views.navigation_user_info, name="navigation"),
    # Ordering
    path("get-lawyer-info/<int:lawyer_id>", views.retain_lawyer, name="lawyer_info"),
    path("create-case/<int:lawyer_id>", CreateCaseView.as_view(), name="create_case"),
    path("lawyer-already-taken/", views.lawyer_already_taken, name="lawyer_already_taken"),
    # Feedback
    path("post-feedback/<int:lawyer_id>/", views.feedback_handler, name="post_feedback"),
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
