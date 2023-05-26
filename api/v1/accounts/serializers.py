import json
import requests
import geocoder
# from pprint import pprint

from django.http.request import HttpRequest

from rest_framework import serializers

from accounts.models import User, UserSession
from general.encryptions import encrypt, decrypt
from general.functions import get_client_ip


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
        request:HttpRequest = kwargs.get("request")
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

        client_ip = get_client_ip(request)

        if response.status_code == 200:
            location = geocoder.ip(client_ip)

            system_meta = request.META.get("HTTP_USER_AGENT")
            system = request.headers.get("Sec-Ch-Ua-Platform")

            is_main_exists = False

            if user.sessions.filter(is_main=True,is_deleted=False).exists():
                is_main_exists = True

            user_session = UserSession.objects.create(
                user=user,
                ip=client_ip,
                country=location.country,
                state=location.state,
                location=location.city,
                system=system,
                system_meta_data=system_meta,
            )

            if not is_main_exists:
                user_session.is_main = True
                user_session.save()

            return {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "email":user.email,
                    "username":user.username,
                    "refresh": response.json().get("refresh"),
                    "access": response.json().get("access"),
                    "session_id": user_session.id,
                }       
            }
        return {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message": "Token generation failed"
                }       
            }