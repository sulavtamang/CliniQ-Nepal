from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Clinic Admin',
        STAFF = 'STAFF', 'Clinic Staff',
        PATIENT = 'PATIENT', 'Patient'

    email = models.EmailField(unique=True)
    phone_number = models.CharField(blank=True, max_length=15)
    role = models.CharField(
        max_length=20, 
        blank=True, 
        choices=Role.choices,
        default=Role.PATIENT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} - {self.get_role_display()}'
        

