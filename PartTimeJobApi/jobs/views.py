from rest_framework import viewsets, generics, filters, status, parsers,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs.models import JobCategory, Job, Requirement, Benefit, Company, Follow, CV
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

class CompanyViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'verification':
            return [perms.IsEmployer()]
        if self.action == 'follow':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    @action(detail=False, methods=['post'], url_path='verification')
    def verification(self, request):
        company = Company.objects.filter(user=request.user).first()

        if not company:
            return Response(status=status.HTTP_404_NOT_FOUND)

        company.is_verified = True
        company.save()
        return Response(status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        if request.user.role != 'CANDIDATE':
            return Response({"detail": "Chỉ ứng viên mới có thể theo dõi công ty."},status=status.HTTP_403_FORBIDDEN)

        company = self.get_object()

        follow_obj, created = Follow.objects.get_or_create(user=request.user, company=company)

        if not created:
            follow_obj.delete()
            return Response({"message": f"Đã bỏ theo dõi {company.name}"},status=status.HTTP_200_OK)

        return Response({"message": f"Đã theo dõi {company.name}"},
                        status=status.HTTP_201_CREATED)

class CVViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CV.objects.filter(is_active=True)
    serializer_class = serializers.CVSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user).order_by('-created_at')
        return self.queryset.none()

    def create(self, request):
        if request.user.role != 'CANDIDATE':
            return Response(
                {"detail": "Chỉ tài khoản Ứng viên mới có thể tạo CV."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cv = serializer.save(user=request.user)

        return Response(self.serializer_class(cv).data, status=status.HTTP_201_CREATED)
