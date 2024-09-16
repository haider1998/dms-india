from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor

class CustomUserCreationForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=15)
    is_patient = forms.BooleanField(required=False)
    is_doctor = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('mobile_number',)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'date_of_birth', 'gender'] 

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'date_of_birth', 'gender']
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number', 'contact_information']



