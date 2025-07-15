from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, MedicalNote

class PatientSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.PATIENT
        if commit:
            user.save()
        return user

class MedecinSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.MEDECIN
        if commit:
            user.save()
        return user

class MedicalNoteForm(forms.ModelForm):
    class Meta:
        model = MedicalNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name']