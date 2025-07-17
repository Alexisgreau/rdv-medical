from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, MedicalNote

class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        (User.Roles.PATIENT, "Patient"),
        (User.Roles.MEDECIN, "Médecin"),
    ]

    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
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