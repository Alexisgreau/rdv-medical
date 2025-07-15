from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Appointment, MedicalNote

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # On étend les fieldsets existants pour y inclure role & phone
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rôle & contact', {
            'fields': ('role', 'phone'),
        }),
    )
    # Idem pour le formulaire d'ajout
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Rôle & contact', {
            'fields': ('role', 'phone'),
        }),
    )
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']

# On enregistre aussi les autres modèles
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'scheduled_time', 'status']

@admin.register(MedicalNote)
class MedicalNoteAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'created_at']
