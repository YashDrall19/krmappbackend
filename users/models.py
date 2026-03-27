from django.db import models

# Create your models here.
from django.db import models
from datetime import date

from django.db import models
from datetime import date

class User(models.Model):
    # 🔑 Unique user ID
    user_id = models.CharField(max_length=10, unique=True, blank=True, null=True)

    # 🔐 Google identity
    google_id = models.CharField(max_length=255, unique=True)

    # 👤 Basic info
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )

    # 📏 Physical details
    weight = models.FloatField(null=True, blank=True)   # in kg
    height = models.FloatField(null=True, blank=True)   # in cm

    # 🖼️ Profile picture (Google URL)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    # 🧠 Health history
    past_illness = models.JSONField(default=list, blank=True)
    past_symptoms = models.JSONField(default=list, blank=True)
    allergy = models.CharField(max_length=255, blank=True)

    # 👨‍👩‍👧 Family history
    family_disease = models.JSONField(default=dict, blank=True)
    # expected format:
    # {
    #   "father": [],
    #   "mother": [],
    #   "siblings": []
    # }

    # 🏃 Lifestyle
    job_type = models.CharField(max_length=100, blank=True)
    water_consumption = models.CharField(max_length=50, blank=True)
    coffee_tea = models.CharField(max_length=50, blank=True)
    smoking = models.CharField(max_length=50, blank=True)
    alcohol = models.CharField(max_length=50, blank=True)
    sleep_hours = models.CharField(max_length=50, blank=True)
    stress_level = models.CharField(max_length=50, blank=True)

    # ⏱️ Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔢 Age calculation
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    # 🔄 Override save to auto-generate user_id
    def save(self, *args, **kwargs):
        if not self.user_id:
            last_user = User.objects.order_by('-id').first()
            if last_user and last_user.user_id:
                last_number = int(last_user.user_id.replace('KRMAPP', ''))
                new_number = last_number + 1
            else:
                new_number = 1
            self.user_id = f"KRMAPP{new_number:04d}"  # format: KRMAPP0001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'user'