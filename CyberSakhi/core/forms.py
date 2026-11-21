from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import IncidentReport

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ["category", "title", "description", "incident_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Describe what happened. Do not include passwords, OTPs or bank details."}),
            "incident_date": forms.DateInput(attrs={"type": "date"}),
        }

from .models import SafetyChecklist

class SafetyChecklistForm(forms.ModelForm):
    class Meta:
        model = SafetyChecklist
        fields = ["mfa_enabled", "unique_passwords", "device_lock", "software_updated", "backups_enabled", "recovery_options"]
        labels = {
            "mfa_enabled": "I have enabled multi-factor authentication on important accounts",
            "unique_passwords": "I use unique, strong passwords for important accounts",
            "device_lock": "My phone and computer have a secure screen lock",
            "software_updated": "My operating system and apps are kept up to date",
            "backups_enabled": "I keep backups of important files",
            "recovery_options": "My account recovery email and phone number are current",
        }
