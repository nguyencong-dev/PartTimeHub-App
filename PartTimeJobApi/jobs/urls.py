from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from jobs import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='companies')

urlpatterns = [
    path('', include(router.urls))
]