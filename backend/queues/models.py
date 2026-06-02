from email.policy import default
from django.utils import choices
from concurrent.futures._base import CANCELLED
from django.db import models
from clinics.models import Doctor

class Token(models.Model):
    class TokenStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending/Waiting'
        CALLED = 'CALLED', 'Called/Active'
        COMPLETED = 'COMPLETED', 'Completed'
        NO_SHOW = 'NO_SHOW', 'NO Show'
        CANCELLED = 'CANCELLED', 'Cancelled'

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='tokens')
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=15)
    token_number = models.PositiveIntegerField()
    booking_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=TokenStatus.choices,
        default=TokenStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        #enforces that token numbers start at 1 per doctor per date
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'booking_date', 'token_number'],
                name='unique_doctor_date_token'
            )
        ]

    def __str__(self):
        return f'Token #{self.token_number} - Dr.{self.doctor.last_name} ({self.patient_name})'

    