from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from jobs import views
router = DefaultRouter()
router.register(r'job-categories', views.JobCategoryViewSet, basename='JobCategory')
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'cvs', views.CVViewSet, basename='cv')

urlpatterns = [
    path('', include(router.urls))
]