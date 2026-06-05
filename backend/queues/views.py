from django.db import transaction, IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from clinics.models import Schedule
from queues.models import Token
from  queues.serializers import TokenSerializer

class BookTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        doctor = serializer.validated_data['doctor']
        patient_name = serializer.validated_data['patient_name']
        patient_phone = serializer.validated_data['patient_phone']
        
        today = timezone.localdate()
        weekday = today.weekday() # Monday:0, Sunday: 6 
        # Adjust weekday to match model's choices: Sunday:0, Monday:1, ... 
        day_index = (weekday + 1) % 7 

        # 1. Verify Doctor has a schedule today
        schedule = Schedule.objects.filter(doctor=doctor, day_of_week=day_index).first()
        if not schedule:
            return Response({"error": "Doctor is not scheduled to work today."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Wrap calculation & creation in transaction block for database-level atomicity
            with transaction.atomic():
                # 2. Count existing tokens booked for this doctor today (and acquire row lock)
                existing_tokens = Token.objects.filter(
                    doctor=doctor, 
                    booking_date=today
                ).select_for_update()

                count = existing_tokens.count()

                # 3. Check if queue is full
                if count >= schedule.max_patients:
                    return Response({"error": "Tokens are fully booked for today."}, status=status.HTTP_400_BAD_REQUEST)

                # 4. Determine next token number
                next_token_number = count + 1

                # 5. Create Token
                token = Token.objects.create(
                    doctor=doctor,
                    patient_name=patient_name,
                    patient_phone=patient_phone,
                    token_number=next_token_number,
                    booking_date=today,
                    status=Token.TokenStatus.PENDING
                )
            response_serializer = TokenSerializer(token)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Fallback if a simultaneous transaction sneaks in despite lock
            return Response({"error": "Booking collision occurred. Please try again."}, status=status.HTTP_409_CONFLICT)
