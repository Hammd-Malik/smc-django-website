from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class doctor_detail(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)
    doctorPicture = models.ImageField(upload_to='doctorPics')
    houspitalName = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    services = models.TextField(max_length=500)
    meeting_link = models.URLField(blank=True)

class blogs(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='blogThumbnail')
    content = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    








