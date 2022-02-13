from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import UserViewSet, ReportVersionLCView, ReportLCView, ReportUserLCView
from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', UserViewSet)

reportversion_urls = [
    path("", ReportVersionLCView.as_view(), name="lc"),
]

reports_urls = [
    path("", ReportLCView.as_view(), name="lc"),
]

reportuser_urls = [
    path("", ReportUserLCView.as_view(), name="lc")
]

urlpatterns = [
    path('', include(router.urls)),
    path("reportversion/", include((reportversion_urls, "loginSystem"), namespace="reportversion")),
    path("reports/", include((reports_urls, "loginSystem"), namespace="reports")),
    path("reportuser/", include((reportuser_urls, "loginSystem"), namespace="reportuser")),
]
