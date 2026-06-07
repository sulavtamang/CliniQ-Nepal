from rest_framework import generics
from rest_framework.permissions import AllowAny
from clinics.models import Doctor
from clinics.serializers import DoctorSerializer

#generic view for listing active doctors publicly
class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (AllowAny,)