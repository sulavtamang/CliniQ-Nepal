from rest_framework import serializers
from accounts.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'password']
    
    def create(self, validated_data):
        # create the user using djanog's built-in password hashing mechanism
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data.get('phone_number', ''),
            role = validated_data.get('role', CustomUser.Role.PATIENT),
            password = validated_data['password']
        )
        return user