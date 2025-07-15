from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        PATIENT = 'PAT', 'Patient'
        MEDECIN = 'DOC', 'Médecin'
        ADMIN = 'ADM', 'Administrateur'

    role = models.CharField(
        max_length=3,
        choices=Roles.choices,
        default=Roles.PATIENT,
    )
    phone = models.CharField(max_length=15, blank=True)

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'PEND', 'En attente'
        CONFIRMED = 'CONF', 'Confirmé'
        CANCELED  = 'CANC', 'Annulé'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_as_patient'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_as_doctor'
    )
    scheduled_time = models.DateTimeField()
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} @ {self.scheduled_time}"

class MedicalNote(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='note'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note pour RDV #{self.appointment.id}"
