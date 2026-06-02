from django.conf import settings
from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clinics')

    def __str__(self):
        return f'{self.name} - {self.address}'

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.specialty}'
    

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')
        ]
    )
    
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.PositiveIntegerField()
    avg_consultation_minutes = models.PositiveIntegerField(default=15)

    def __str__(self):
        return f'{self.doctor} - {self.day_of_week} - {self.start_time} to {self.end_time}'
