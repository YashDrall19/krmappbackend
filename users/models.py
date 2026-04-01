from django.db import models
from datetime import date

class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True, blank=True, null=True)

    google_id = models.CharField(max_length=255, unique=True)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'M'), ('F', 'F'), ('O', 'O')],
        blank=True
    )

    weight = models.FloatField(null=True, blank=True)   # in kg
    height = models.FloatField(null=True, blank=True)   # in cm

    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    past_illness = models.JSONField(default=list, blank=True)
    past_symptoms = models.JSONField(default=list, blank=True)
    allergy = models.CharField(max_length=255, blank=True)

    family_disease = models.JSONField(default=dict, blank=True)

    job_type = models.CharField(max_length=100, blank=True)
    water_consumption = models.CharField(max_length=50, blank=True)
    coffee_tea = models.CharField(max_length=50, blank=True)
    smoking = models.CharField(max_length=50, blank=True)
    alcohol = models.CharField(max_length=50, blank=True)
    sleep_hours = models.CharField(max_length=50, blank=True)
    stress_level = models.CharField(max_length=50, blank=True)

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

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