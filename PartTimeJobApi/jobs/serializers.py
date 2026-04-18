from rest_framework import serializers
from jobs.models import JobCategory, Job, Requirement, Benefit, Company, CV, Application, Message, Notification, Review, \
    User, CompanyImage


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id', 'subject', 'description']


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ['id', 'subject']


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.avatar:
            data['avatar'] = instance.avatar.url
        return data


class CompanySerializer(ItemSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'avatar', 'description', 'tax_code', 'status']

        extra_kwargs = {
            'description': {
                'write_only': True
            },
            'tax_code': {
                'write_only': True
            },
            'status': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'salary', 'working_time', 'location', 'category', 'company']
        read_only_fields = ['company']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['company'] = request.user.company
        return super().create(validated_data)


class JobDetailsSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    benefits = BenefitSerializer(many=True, read_only=True)

    class Meta:
        model = JobSerializer.Meta.model
        fields = JobSerializer.Meta.fields + ['requirements', 'benefits']


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'file', 'description', 'created_at']
        read_only_fields = ['user']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'user', 'cv', 'status', 'created_at']
        read_only_fields = ['user']


class CompanyDetailSerializer(ItemSerializer):
    jobs = JobSerializer(many=True, read_only=True, source='job_set')

    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'description', 'jobs', 'avatar']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['user']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer',
            'reviewer_name',
            'target_company',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Số sao đánh giá phải từ 1 đến 5.')
        return value


class SimpleUserSerializer(ItemSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']


class UserSerializer(SimpleUserSerializer):
    class Meta:
        model = SimpleUserSerializer.Meta.model
        fields = SimpleUserSerializer.Meta.fields + ['id', 'username', 'password', 'avatar', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError("Bạn không được phép đăng ký tài khoản ADMIN.")
        return value

    def create(self, validated_data):
        role = validated_data.get('role', User.Role.CANDIDATE)

        if role not in [User.Role.CANDIDATE, User.Role.EMPLOYER]:
            raise serializers.ValidationError("Role không hợp lệ. Chỉ được chọn CANDIDATE hoặc EMPLOYER.")

        user = User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user

class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyImage
        fields = ['id','company', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url
        return data