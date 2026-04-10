from rest_framework import viewsets, generics, filters, status, parsers,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs.models import JobCategory, Job, Requirement, Benefit, Application, CV
from jobs import serializers, perms


class JobCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = serializers.JobCategorySerializer

class JobViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Job.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method.__eq__("POST"):
            return [perms.IsEmployer()]
        elif self.request.method.__eq__('PATCH') or self.request.method.__eq__('DELETE'):
            return [perms.IsOwnerEmployer()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action.__eq__('retrieve'):
            return serializers.JobDetailsSerializer
        return serializers.JobSerializer

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get('q')
        if q:
            query = query.filter(title__icontains=q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)
        from_sal = self.request.query_params.get('from_salary')
        if from_sal:
            query = query.filter(salary__gte=from_sal)
        to_sal = self.request.query_params.get('to_salary')
        if to_sal:
            query = query.filter(salary__lte=to_sal)

        return query

    def create(self, request):
        if not hasattr(request.user, 'company'):
            return Response({"detail": "Bạn phải tạo hồ sơ Công ty trước khi đăng việc."},
                            status=status.HTTP_400_BAD_REQUEST)
        s = serializers.JobSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        job = s.save(company=request.user.company)
        return Response(serializers.JobDetailsSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'patch'], url_path='requirements', detail=True)
    def requirements(self, request, pk):
        job = self.get_object()
        if request.method.__eq__('POST'):
            is_many = isinstance(request.data, list)
            s = serializers.RequirementSerializer(data=request.data, many=is_many)
            s.is_valid(raise_exception=True)
            s.save(job=job)
            return Response(s.data, status = status.HTTP_201_CREATED)
        elif request.method.__eq__('PATCH'):
            requirement_id = request.data.get('id')
            requirement = Requirement.objects.get(id = requirement_id, job=job)
            s = serializers.RequirementSerializer(requirement, data = request.data, partial=True)
            s.is_valid(raise_exception=True)
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'patch'], url_path='benefits', detail=True)
    def benefits(self, request, pk):
        job = self.get_object()
        if request.method.__eq__('POST'):
            is_many = isinstance(request.data, list)
            s = serializers.BenefitSerializer(data=request.data, many=is_many)
            s.is_valid(raise_exception=True)
            s.save(job=job)
            return Response(s.data, status = status.HTTP_201_CREATED)
        elif request.method.__eq__('PATCH'):
            benefit_id = request.data.get('id')
            benefit = Benefit.objects.get(id=benefit_id, job=job)
            s = serializers.BenefitSerializer(benefit, data=request.data, partial=True)
            s.is_valid(raise_exception=True)
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='apply', detail=True)
    def apply(self, request, pk):
        if request.user.role != 'CANDIDATE':
            return Response({"detail":"Chỉ ứng viên mới có thể ứng tuyển."}, status=status.HTTP_403_FORBIDDEN)
        job = self.get_object()
        cv_id = request.data.get('cv_id')

        cv = CV.objects.filter(id=cv_id, user=request.user).first()
        if not cv:
            return Response({"detail":"CV không hợp lệ hoặc không thuộc về bạn."}, status=status.HTTP_400_BAD_REQUEST)

        app, created = Application.objects.get_or_create(job=job, user=request.user, defaults={'cv': cv, 'status': 'PENDING'})

        if not created:
            return Response({"detail": "Bạn đã nộp đơn cho công việc này rồi."}, status=status.HTTP_400_BAD_REQUEST)

        s = serializers.ApplicationSerializer(app)
        return Response(s.data, status=status.HTTP_201_CREATED)

class ApplicationViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user