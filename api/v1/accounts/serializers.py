from rest_framework import serializers

from accounts.models import User
from general.encryptions import encrypt


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'required':'Please enter your email address',"invalid":"Please enter a valid email address"})
    password = serializers.CharField(max_length=18,error_messages={'required':'Please enter your password'})

    def validate(self, attrs):
        super().validate(attrs)

        email = attrs.get('email')

        if User.objects.filter(email=email,is_deleted=False).exists():
            raise serializers.ValidationError({"email":"Email already exists"})

        return attrs
    
    def save(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        
        profile = User.objects.create_user(email=email,password=password,encrypted_password=encrypt(password))

        return profile