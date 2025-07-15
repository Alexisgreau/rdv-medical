from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

# **Importer explicitement** ton module views
from app.views import (
    PatientSignUpView, MedecinSignUpView,
    PatientDashboardView, UserProfileUpdateView,
    HomePageView, 
    DoctorAppointmentListView, DoctorAppointmentDetailView
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('accounts/login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/patient/', PatientSignUpView.as_view(),   name='signup_patient'),
    path('accounts/signup/medecin/', MedecinSignUpView.as_view(),   name='signup_medecin'),
    path('dashboard/patient/',     PatientDashboardView.as_view(), name='dashboard_patient'),
    path("medecin/rdvs/",      DoctorAppointmentListView.as_view(),   name="medecin_rdvs"),
    path("medecin/rdvs/<int:pk>/", DoctorAppointmentDetailView.as_view(), name="medecin_appointment_detail"),
    path('dashboard/medecin/', DoctorAppointmentListView.as_view(), name='dashboard_medecin'),
    path('api/', include(router.urls)),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
]
