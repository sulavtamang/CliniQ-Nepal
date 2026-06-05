from rest_framework import serializers
from clinics.models import Clinic, Doctor, Schedule

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class ScheduleSerialzer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'day_of_week', 'day_name', 'start_time', 'end_time', 'max_patients', 'avg_consultation_minutes']

class DoctorSerialzier(serializers.ModelSerializer):
    schedules = ScheduleSerialzer(many=True, read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialty', 'is_active', 'clinic_name', 'schedules']