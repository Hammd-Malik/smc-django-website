from email.policy import default
from django.db import models

# Create your models here.

class inquiries(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=300)
    status = models.IntegerField(default=0)
    message = models.TextField()



