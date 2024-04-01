# import rest_framework.authtoken.views
# from django.urls import path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register("clients-api", views.ClientViewSet, "clients")
router.register("lawyers-api", views.LawyerViewSet, "lawyers")
router.register("cases-api", views.CaseViewSet, "cases")

urlpatterns = router.urls
