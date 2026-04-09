from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from jobs import views
router = DefaultRouter()
router.register('job-categories', views.JobCategoryViewSet, basename='JobCategory')
router.register('jobs', views.JobViewSet, basename='job')
router.register('companies', views.CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls))
]