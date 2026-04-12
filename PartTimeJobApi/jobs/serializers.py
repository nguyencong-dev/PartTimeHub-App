from rest_framework import serializers
from jobs.models import JobCategory, Job, Requirement, Benefit, Company, CV, Application, Message, Notification


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
        if instance.image:
            data['image'] = instance.image.url
        return data

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']


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

class CompanyDetailSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True, source='job_set')

    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'description', 'jobs']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['user']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user']