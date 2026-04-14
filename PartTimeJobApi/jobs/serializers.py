from rest_framework import serializers
from jobs.models import JobCategory, Job, Requirement, Benefit, Company, CV, Application, Message, Notification, Review


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
        fields = ['id', 'name', 'address', 'avatar']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'salary', 'working_time', 'location', 'category','company']
        read_only_fields = ['company']
class JobDetailsSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    benefits = BenefitSerializer(many=True,read_only=True)
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