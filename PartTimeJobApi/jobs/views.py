from rest_framework import viewsets, generics
from jobs import serializers
from jobs.models import JobCategory, Company


class CompanyViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer