from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PatientForm, DoctorForm, PatientProfileForm, DoctorProfileForm
from .models import Patient, Doctor

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_patient = user_form.cleaned_data['is_patient']
            user.is_doctor = user_form.cleaned_data['is_doctor']
            user.save()

            if user.is_patient:
                patient_form = PatientForm(request.POST, instance=Patient(user=user))
                if patient_form.is_valid():
                    patient_form.save()
            elif user.is_doctor:
                doctor_form = DoctorForm(request.POST, instance=Doctor(user=user))
                if doctor_form.is_valid():
                    doctor_form.save()

            # Handle mobile number verification (OTP) here (we'll add this later)

            login(request, user)
            return redirect('home') # Redirect to a home page or dashboard
    else:
        user_form = CustomUserCreationForm()
        patient_form = PatientForm()
        doctor_form = DoctorForm()
    return render(request, 'dms/register.html', {'user_form': user_form, 'patient_form': patient_form, 'doctor_form': doctor_form})

@login_required
def profile(request):
    if request.user.is_patient:
        patient = request.user.patient
        # Add logic for patient profile
    elif request.user.is_doctor:
        doctor = request.user.doctor
        # Add logic for doctor profile
    return render(request, 'dms/profile.html')

@login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_profile') # Replace with your actual profile view name or URL
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'dms/patient_profile.html', {'form': form})
@login_required
def doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile') # Replace with your actual profile view name or URL 
    else:
        form = DoctorProfileForm(instance=doctor)
    return render(request, 'dms/doctor_profile.html', {'form': form})
