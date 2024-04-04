from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-list/", views.lawyers_list, name="list"),
    path("lawyer-profile/", views.LawyerProfile.as_view(), name="lawyer_profile"),
    path("client-profile/", views.ClientProfile.as_view(), name="client_profile"),
]
