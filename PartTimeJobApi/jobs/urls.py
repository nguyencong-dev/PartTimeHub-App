from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls))
]