from rest_framework import serializers
from queues.models import Token

class TokenSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.last_name', read_only=True)

    class Meta:
        model = Token
        fields = ['id', 'doctor', 'doctor_name', 'patient_name', 'patient_phone', 'token_number', 'booking_date', 'status', 'created_at', 'called_at']
        read_only_fields = ['token_number', 'created_at', 'called_at']
    
    def get_doctor_name(self, obj):
        return f'Dr. {obj.doctor.first_name} {obj.doctor.last_name}'