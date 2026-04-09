from rest_framework import serializers
from jobs.models import JobCategory, Job, Requirement, Benefit, Company

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

class JobDetailsSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    benefits = BenefitSerializer(many=True,read_only=True)
    class Meta:
        model = JobSerializer.Meta.model
        fields = JobSerializer.Meta.fields + ['requirements', 'benefits']
