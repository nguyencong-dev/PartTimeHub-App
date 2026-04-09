from rest_framework import viewsets, generics, filters, status, parsers,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs.models import JobCategory, Job
from jobs import serializers, perms


class JobCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = serializers.JobCategorySerializer

class JobViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = serializers.JobDetailsSerializer

    # def get_permissions(self):
    #     if self.request.method.__eq__("POST"):
    #         return [perms.IsEmployer()]
    #     return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.JobDetailsSerializer
        return serializers.JobSerializer

    def create(self, request):
        s = serializers.JobSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        job = s.save()

        return Response(serializers.JobDetailsSerializer(job).data, status=status.HTTP_201_CREATED)

