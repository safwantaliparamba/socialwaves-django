import json
import requests
# from pprint import pprint

from rest_framework import serializers

from accounts.models import User
from general.encryptions import encrypt, decrypt


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128,min_length=4,error_messages={'required':'Please enter your name'})
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
        name = self.validated_data.get("name")
        
        profile = User.objects.create_user(name=name,email=email,password=password,encrypted_password=encrypt(password),username=email)

        return profile
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'required':'Please enter your email address',"invalid":"Please enter a valid email address"})
    password = serializers.CharField(max_length=18,error_messages={'required':'Please enter your password'})

    def validate(self, attrs):
        super().validate(attrs)

        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"Email not found"})
        else:
            user:User = User.objects.filter(email=email).latest("date_joined")

            if not user.is_email_verified:
                raise serializers.ValidationError({"email":"Please verify your email address"})
            else:
                if not decrypt(user.encrypted_password) == password:
                    raise serializers.ValidationError({"password":"Incorrect password"})

        return attrs
    
    def save(self, **kwargs):
        request = kwargs.get("request")
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")

        user: User = User.objects.filter(email=email,is_deleted=False).latest("date_joined")
        
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "email": email,
            "password": password,
        }

        protocol = "http://"

        if request.is_secure():
            protocol = "https://"

        host = request.get_host()
        url = protocol + host + "/api/v1/accounts/token/"
        
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "email":user.email,
                    "username":user.username,
                    "refresh": response.json().get("refresh"),
                    "access": response.json().get("access"),
                }       
            }
        return {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message": "Token generation failed"
                }       
            }