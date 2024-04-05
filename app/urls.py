from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-list/", views.lawyers_list, name="list"),
    path("lawyer-profile/", views.lawyer_profile, name="lawyer_profile"),
    path("client-profile/", views.client_profile, name="client_profile"),
    path("edit-lawyer-profile/", views.edit_lawyer_profile, name="edit_lawyer"),
    path("edit-client-profile/", views.edit_client_profile, name="edit_client"),
]
