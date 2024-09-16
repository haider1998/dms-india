from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model extending Django's default User.
    This allows for future role-based customization (Doctor/Patient).
    """
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username  # Or use email if that's your preference

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  # Choices can be added later
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    contact_information = models.TextField(null=True, blank=True)  # Additional contact details

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class DoctorPatientAssociation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient') 

    def __str__(self):
        return f"{self.doctor.user.username} - {self.patient.user.username}"

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.TextField()  # Detailed dosage instructions
    duration = models.CharField(max_length=100)  # E.g., "7 days", "2 weeks"
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.user.username} by {self.doctor.user.username}"

class Diagnosis(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    details = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Diagnosis for {self.patient.user.username} on {self.date}"

class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Doctor or Patient can upload
    file = models.FileField(upload_to='reports/')  # Use 'MEDIA_ROOT' setting for storage
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.user.username} uploaded on {self.upload_date}"

