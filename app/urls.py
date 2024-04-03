from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-list/", views.lawyers_list, name="list"),
    path("create/", views.add_lawyer, name="new-lawyer"),
]
