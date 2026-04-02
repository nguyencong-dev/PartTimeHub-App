from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN',
        EMPLOYER = 'EMPLOYER',
        CANDIDATE = 'CANDIDATE',

    class Status(models.TextChoices):
        PENDING = 'PENDING',
        ACTIVE = 'ACTIVE',
        BLOCKED = 'BLOCKED',

    avatar = CloudinaryField(null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CANDIDATE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.username


class Company(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING',
        APPROVED = 'APPROVED',
        REJECTED = 'REJECTED',

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tax_code = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.name


class CompanyImage(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = CloudinaryField(null=True)

class CompanyVerification(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING',
        VERIFIED = 'VERIFIED',
        REJECTED = 'REJECTED',

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verified_at = models.DateTimeField(null=True, blank=True)


class JobCategory(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Job(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    working_time = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Requirement(BaseModel):
    subject = models.CharField(max_length=255, null=False)
    description = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='requirements',null=True)

    def __str__(self):
        return self.subject

class CV(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='cvs/')
    description = models.TextField(blank=True)


class Application(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING',
        ACCEPTED = 'ACCEPTED',
        REJECTED = 'REJECTED',

    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)


class Follow(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Review(BaseModel):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews_authored')
    target_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews_received')
    rating = models.IntegerField()
    comment = models.TextField()


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_messages')
    content = models.TextField()
