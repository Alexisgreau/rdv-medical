from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Appointment, MedicalNote

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'patient', 'doctor', 'scheduled_time', 'status')
    list_filter   = ('status', 'doctor')
    search_fields = ('patient__username', 'doctor__username')
    ordering      = ('-scheduled_time',)

@admin.register(MedicalNote)
class MedicalNoteAdmin(admin.ModelAdmin):
    list_display  = ('appointment', 'snippet')
    search_fields = ('appointment__patient__username',)
    
    def snippet(self, obj):
        return obj.content[:50] + ('…' if len(obj.content) > 50 else '')
    snippet.short_description = 'Contenu (aperçu)'
