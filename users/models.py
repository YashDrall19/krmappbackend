from django.db import models

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=100, blank=False)
  phone_number = models.CharField(max_length=15, blank=False)