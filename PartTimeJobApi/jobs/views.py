from rest_framework import viewsets, generics, filters, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs.models import JobCategory, Job, Requirement, Benefit, Company, Follow, CV, Application, Message, Notification, \
    Review
from jobs import serializers, perms
from jobs.perms import IsEmployer
from jobs.serializers import ApplicationSerializer
from django.db.models import Q


class JobCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = serializers.JobCategorySerializer


class JobViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Job.objects.filter(is_active=True)

    def get_permissions(self):

        if self.action in ['requirements', 'benefits']:
            if self.request.method.__eq__("POST") or self.request.method.__eq__('PATCH') or self.request.method.__eq__(
                    'DELETE'):
                return [perms.IsOwnerEmployer()]
        elif self.action in ['destroy', 'job_applications']:
            return [perms.IsOwnerEmployer()]
        elif self.action == 'create':
            return [perms.IsEmployer()]
        elif self.action in ['apply_job']:
            return [perms.IsCandidate()]
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
            return Response(s.data, status=status.HTTP_201_CREATED)
        elif request.method.__eq__('PATCH'):
            requirement_id = request.data.get('id')
            requirement = Requirement.objects.get(id=requirement_id, job=job)
            s = serializers.RequirementSerializer(requirement, data=request.data, partial=True)
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
            return Response(s.data, status=status.HTTP_201_CREATED)
        elif request.method.__eq__('PATCH'):
            benefit_id = request.data.get('id')
            benefit = Benefit.objects.get(id=benefit_id, job=job)
            s = serializers.BenefitSerializer(benefit, data=request.data, partial=True)
            s.is_valid(raise_exception=True)
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=True, url_path='apply', parser_classes=[parsers.MultiPartParser])
    def apply_job(self, request, pk):
        job = self.get_object()
        user = request.user

        file = request.FILES.get('cv_file')
        cv_id = request.data.get('cv_id')

        if not file and not cv_id:
            return Response("Vui lòng đính kèm file CV mới  hoặc chọn CV có sẵn.",
                            status=status.HTTP_400_BAD_REQUEST)
        cv = None
        if cv_id:
            try:
                cv = CV.objects.get(id=cv_id, user=user, is_active=True)
            except CV.DoesNotExist:
                return Response("CV không tồn tại hoặc không thuộc quyền sở hữu của bạn.",
                                status=status.HTTP_404_NOT_FOUND)

        elif file:
            desc = request.data.get('description', f'CV ứng tuyển {job.title}')
            cv = CV.objects.create(user=user, file=file, description=desc)

        apply = Application.objects.filter(job=job, user=user).first()

        if apply:
            apply.cv = cv
            apply.status = Application.Status.PENDING
            apply.save()
            return Response(serializers.ApplicationSerializer(apply).data, status=status.HTTP_200_OK)

        s = serializers.ApplicationSerializer(data={'job': job.id, 'cv': cv.id})
        s.is_valid(raise_exception=True)
        apply = s.save(user=user)

        return Response(serializers.ApplicationSerializer(apply).data, status=status.HTTP_201_CREATED)


    @action(methods=['get'], detail=True, url_path='applications')
    def job_applications(self, request, pk):
        job = self.get_object()
        applications = Application.objects.filter(job=job)
        s = serializers.ApplicationSerializer(applications, many=True)
        return Response(s.data, status=status.HTTP_200_OK)


class CompanyViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CompanySerializer
        return serializers.CompanyDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'verification':
            return [perms.IsEmployer()]
        if self.action == 'follow':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path='verification')
    def verification(self, request):

        user = request.user
        if user.role != 'EMPLOYER':
            return Response({"detail": "Chỉ EMPLOYER mới được làm việc này."}, status=403)

        try:
            company = user.company
        except Company.DoesNotExist:
            return Response({"detail": "Bạn chưa có hồ sơ công ty."}, status=400)

        if company.is_verified:
            return Response({"detail": "Đã xác thực trước đó."}, status=400)

        company.is_pending_verification = True
        company.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        if request.user.role != 'CANDIDATE':
            return Response({"detail": "Chỉ ứng viên mới có thể theo dõi công ty."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, url_path='follow')
    def follow(self, request, pk=None):
        company = self.get_object()
        user = request.user

        if user.role != 'CANDIDATE':
            return Response({"detail": "Chỉ ứng viên mới có thể theo dõi công ty."},
                            status=status.HTTP_403_FORBIDDEN)

        follow_obj, created = Follow.objects.get_or_create(user=user, company=company)

        if not created:
            follow_obj.delete()
            return Response({"detail": "Đã bỏ theo dõi công ty."}, status=status.HTTP_200_OK)
        return Response({"detail": "Đã theo dõi công ty thành công!"}, status=status.HTTP_201_CREATED)


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


class ApplicationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.action in ['list', 'status']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return self.queryset.none()
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'CANDIDATE':
            return self.queryset.filter(user=user).order_by('-created_at')

        return self.queryset.filter(job__company__user=user).select_related('job', 'cv', 'user')

    @action(methods=['patch'], detail=True, url_path='status')
    def status(self, request, pk=None):
        application = self.get_object()

        if not (hasattr(request.user, 'role') and request.user.role == 'EMPLOYER'):
            return Response({"detail": "Chỉ Nhà tuyển dụng mới có quyền này."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.ApplicationSerializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return self.queryset.none()
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_user = serializer.validated_data.get('user')
        if receiver_user == request.user:
            return Response({"detail": "Bạn không thể tự gửi thông báo cho chính mình."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True, url_path='read')
    def read(self, request, pk=None):
        notification = self.get_object()
        if notification.user != request.user:
            return Response({"detail": "Không có quyền."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.role != 'CANDIDATE':
            return Response(
                {
                    "detail": "Chỉ tài khoản ứng viên mới có quyền review!"
                }, status=status.HTTP_403_FORBIDDEN
            )
        target_company = request.data.get('target_company')

        if Review.objects.filter(reviewer=user, target_company=target_company).exists():
            return Response(
                {
                    "detail": "Bạn đã đánh giá cho công ty này rồi!"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
