from django.contrib import admin
from .models import Job, Company, JobCategory, Requirement, CompanyImage, User
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django.urls import path
from django import forms
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone


class JobForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class CompanyImageAdmin(admin.TabularInline):
    model = CompanyImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image_preview', 'image']

    def image_preview(self, obj):
        if obj and obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="150" style="border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />')
        return "Chưa có ảnh"

    image_preview.short_description = "Ảnh xem trước"


class RequirementInline(admin.TabularInline):
    model = Requirement
    extra = 1
    fields = ['subject']


class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'category', 'salary', 'working_time', 'location']
    search_fields = ['title', 'company__name']
    list_filter = ['category', 'is_active']
    inlines = [RequirementInline]

    form = JobForm


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'tax_code', 'status', 'is_active']
    search_fields = ['name', 'tax_code', 'user__username']
    list_filter = ['status', 'is_active']
    list_editable = ['status', 'is_active']

    inlines = [CompanyImageAdmin]


class RequirementAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject']
    list_filter = ['subject']


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']


class MyAdminSite(admin.AdminSite):
    site_header = 'Part Time Hub App'

    def get_urls(self):
        return [
            path('jobs-stats/', self.jobs_stats),
        ] + super().get_urls()

    def jobs_stats(self, request):
        current_year = timezone.now().year

        jobs_qs = (Job.objects.filter(created_at__year=current_year)
                   .annotate(month=TruncMonth('created_at'))
                   .values('month').annotate(count=Count('id')))

        candidates_qs = (User.objects.filter(role=User.Role.CANDIDATE, date_joined__year=current_year)
                         .annotate(month=TruncMonth('date_joined'))
                         .values('month').annotate(count=Count('id')))

        hr_qs = (Company.objects.filter(created_at__year=current_year)
                 .annotate(month=TruncMonth('created_at'))
                 .values('month').annotate(count=Count('id')))

        job_data = [0] * 12
        candidate_data = [0] * 12
        hr_data = [0] * 12

        for item in jobs_qs:
            job_data[item['month'].month - 1] = item['count']

        for item in candidates_qs:
            candidate_data[item['month'].month - 1] = item['count']

        for item in hr_qs:
            hr_data[item['month'].month - 1] = item['count']

        context = {
            'months': json.dumps([f"Tháng {i}" for i in range(1, 13)]),
            'job_data': json.dumps(job_data),
            'candidate_data': json.dumps(candidate_data),
            'hr_data': json.dumps(hr_data),
            'current_year': current_year,
            'title': 'Thống kê tăng trưởng',
            'site_header': self.site_header,
            'has_permission': self.has_permission(request),
        }

        return TemplateResponse(request, 'admin/stats.html', context)


admin_site = MyAdminSite()

admin_site.register(Job, JobAdmin)
admin_site.register(Company, CompanyAdmin)
admin_site.register(JobCategory, JobCategoryAdmin)
admin_site.register(Requirement, RequirementAdmin)
