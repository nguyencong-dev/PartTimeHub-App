from django.contrib import admin

from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django.urls import path
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MyAdminSite(admin.AdminSite):
    site_header = 'Part Time Hub App'

    def get_urls(self):
        return [
            path('jobs-stats/', self.course_stats),
        ] + super().get_urls()

    def course_stats(self, request):
        return TemplateResponse(request, 'admin/stats.html')

admin_site = MyAdminSite()