from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from jobs import views
router = DefaultRouter()
router.register(r'job-categories', views.JobCategoryViewSet, basename='JobCategory')
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'cvs', views.CVViewSet, basename='cv')
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]