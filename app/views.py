from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views import generic
from .forms import SignupForm, MedicalNoteForm, UserProfileForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import DetailView
from .decorators import role_required
from .models import User, Appointment, MedicalNote, Appointment, User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from rest_framework import viewsets, status
from .serializers import AppointmentSerializer
from .permissions import IsPatient, IsOwnerOrDoctor
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime


class SignUpView(generic.CreateView):
    form_class = SignupForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('login')

@method_decorator(role_required(User.Roles.PATIENT), name='dispatch')
class PatientDashboardView(TemplateView):
    template_name = 'dashboard/patient.html'

class HomePageView(TemplateView):
    template_name = "home.html"

@method_decorator(role_required(User.Roles.MEDECIN), name='dispatch')
class DoctorAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'dashboard/medecin_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        date_str = self.request.GET.get('date')
        try:
            if date_str:
                # bien qualifier datetime.strftime sur le module
                sel_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                sel_date = timezone.localdate()
        except ValueError:
            sel_date = timezone.localdate()

        qs = Appointment.objects.filter(
            doctor=self.request.user,
            scheduled_time__date=sel_date
        ).select_related('patient', 'note').order_by('scheduled_time')

        self.selected_date = sel_date
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['selected_date'] = getattr(self, 'selected_date', timezone.localdate())
        return ctx

@method_decorator(role_required(User.Roles.MEDECIN), name='dispatch')
class DoctorAppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'dashboard/medecin_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            note = self.object.note
            form = MedicalNoteForm(instance=note)
        except MedicalNote.DoesNotExist:
            note = None
            form = MedicalNoteForm()
        ctx.update({'note': note, 'form': form})
        return ctx

    def post(self, request, *args, **kwargs):
        appt = self.get_object()
        if request.user != appt.doctor:
            raise PermissionDenied
        # Récupérer ou créer la note
        note, _ = MedicalNote.objects.get_or_create(appointment=appt)
        form = MedicalNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('medecin_appointment_detail', pk=appt.pk)
        return self.render_to_response(self.get_context_data(form=form))
    
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        u = self.request.user
        if u.role == User.Roles.PATIENT:
            return Appointment.objects.filter(patient=u)
        if u.role == User.Roles.MEDECIN:
            return Appointment.objects.filter(doctor=u)
        return Appointment.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsPatient()]
        return [IsOwnerOrDoctor()]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """Endpoint POST /api/appointments/{pk}/confirm/"""
        appt = self.get_object()
        if request.user.role != User.Roles.MEDECIN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        appt.status = Appointment.Status.CONFIRMED
        appt.save()
        return Response(self.get_serializer(appt).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='available-slots')
    def available_slots(self, request):
        """
        GET /api/appointments/available-slots/?doctor=<id>&date=YYYY-MM-DD
        Renvoie la liste ISO des créneaux libres (slots de 30 min entre 09:00 et 17:00).
        """
        doctor_id = request.query_params.get('doctor')
        date_str  = request.query_params.get('date')
        if not doctor_id or not date_str:
            return Response([], status=400)

        try:
            day = datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response([], status=400)

        tz = timezone.get_current_timezone()
        start = datetime.datetime.combine(day, datetime.time(9, 0), tzinfo=tz)
        end   = datetime.datetime.combine(day, datetime.time(17, 0), tzinfo=tz)

        slots = []
        current = start
        delta = datetime.timedelta(minutes=30)
        while current < end:
            # on considère le slot libre si pas de RDV statuts PEND ou CONF overlapping
            if not Appointment.objects.filter(
                    doctor_id=doctor_id,
                    scheduled_time__gte=current,
                    scheduled_time__lt=current + delta
                ).exists():
                slots.append(current.isoformat())
            current += delta

        return Response(slots)
    
class PatientDashboardView(TemplateView):
    template_name = "dashboard/patient.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Tous les RDV du patient
        ctx['appointments'] = Appointment.objects.filter(patient=self.request.user)\
                                                .order_by('scheduled_time')
        # Tous les médecins pour la dropdown
        ctx['doctors'] = User.objects.filter(role=User.Roles.MEDECIN)
        return ctx
    
    def post(self, request, *args, **kwargs):
        # récupère les champs du form standard
        dt = request.POST.get('scheduled_time')
        doc_id = request.POST.get('doctor')
        if dt and doc_id:
            Appointment.objects.create(
                patient=request.user,
                doctor=User.objects.get(pk=doc_id),
                scheduled_time=timezone.datetime.fromisoformat(dt)
            )
        return redirect('dashboard_patient')
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'registration/profile_form.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user