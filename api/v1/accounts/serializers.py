import json
import requests
import geocoder
# from pprint import pprint

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.http.request import HttpRequest

from user_agents import parse
from rest_framework import serializers

from accounts.models import User, UserSession
from general.encryptions import encrypt, decrypt
from general.middlewares import RequestMiddleware
from api.v1.general.functions import generate_image, generate_unique_username
from general.functions import (
    get_client_ip,
    getDomain,
    random_password,
)


def authenticate(email: str, password: str):
    """
     returns authentication credentials using email and password
    """
    request = RequestMiddleware(get_response=None)
    request: HttpRequest = request.thread_local.current_request

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "password": password,
    }

    url = getDomain(request) + "/api/v1/accounts/token/"
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    user: User = User.objects.filter(email=email,is_deleted=False).latest("date_joined")

    if response.status_code == 200:
        is_main_exists = False
        user_session: UserSession | None = None 
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent_data = parse(user_agent)

        if user.sessions.filter(is_main=True,is_active=True,is_deleted=False).exists():
            is_main_exists = True

        ip = None
        browser_name = user_agent_data.browser.family
        browser_version = user_agent_data.browser.version_string
        system = f"{user_agent_data.os.family} {user_agent_data.os.version_string}"

        if settings.DEBUG:
            ip = settings.SYSTEM_IP
        else:
            ip = get_client_ip(request)

        location = geocoder.ip(ip)

        city = location.city
        state = location.state
        country = location.country

        user_session = UserSession.objects.create(
            ip= ip,
            user= user,
            city= city,
            state= state,
            system=  system,
            country= country,
            browser= browser_name,
            is_pc= user_agent_data.is_pc,
            browser_version= browser_version,
            is_mobile= user_agent_data.is_mobile,
        )

        if not is_main_exists:
            user_session.is_main = True
            user_session.save()

        bookmark_count = 2
        notification_count = 129
        is_pro_member = user.membership_type == "pro"
        user_image = generate_image(user.image) if user.image else False

        return {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "email":user.email,
                "name":user.name,
                "username":user.username,
                "refresh": response.json().get("refresh"),
                "access": response.json().get("access"),
                "session_id": user_session.id,
                "is_pro_member": is_pro_member,
                "bookmark_count": bookmark_count,
                "notification_count": notification_count,
                "image": user_image,
            }       
        }
    return {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message": "Token generation failed"
            }       
        }


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128,min_length=4,error_messages={'required':'Please enter your name'})
    email = serializers.EmailField(error_messages={'required':'Please enter your email address',"invalid":"Please enter a valid email address"})
    password = serializers.CharField(max_length=18,error_messages={'required':'Please enter your password'})
    confirm_password = serializers.CharField(max_length=18, error_messages={'required':'Please enter your confirmed password'})

    def validate(self, attrs):
        super().validate(attrs)

        email = attrs.get('email')
        password = attrs.get('password')
        confirmed_password = attrs.get('confirm_password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email":"Email already exists"})
        
        if password != confirmed_password:
            print(password)
            print(confirmed_password)
            raise serializers.ValidationError({"password":"passwords are incorrect"})

        return attrs
    
    def save(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        name = self.validated_data.get("name")

        username = generate_unique_username()
        
        profile = User.objects.create_user(
                name=name,
                email=email,
                password=password,
                username=username
            )
        
        return profile
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'required':'Please enter your email address',"invalid":"Please enter a valid email address"})
    password = serializers.CharField(max_length=18, error_messages={'required':'Please enter your password'})
    # session_id = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        # session_id = attrs.get('session_id')

        if not User.objects.filter(email=email, is_deleted=False).exists():
            raise serializers.ValidationError({"email":"Email not found"})
        else:
            user:User = User.objects.filter(email=email,is_deleted=False).latest("date_joined")

            if not user.is_email_verified:
                raise serializers.ValidationError({"email":"Please verify your email address"})
            else:
                if not decrypt(user.encrypted_password) == password:
                    raise serializers.ValidationError({"password":"Incorrect password"})

        # if session_id and not is_valid_uuid(session_id):
        #     raise serializers.ValidationError({"session_id":"Session id is not a valid uuid"})

        return attrs
    
    def save(self, **kwargs):
        request: HttpRequest = kwargs.get("request")

        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        # session_id = self.validated_data.get("session_id")

        user: User = User.objects.filter(email=email,is_deleted=False).latest("date_joined")
        
        response = authenticate(email, password)

        return response
    

class GoogleAuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=128)
    name  = serializers.CharField(max_length=128)

    def save(self, **kwargs):
        name  = self.validated_data.get("name")
        email = self.validated_data.get("email")

        if not User.objects.filter(email=email,is_deleted=False).exists():
            password = random_password(8)
            username = generate_unique_username()
            
            user = User.objects.create_user(
                name=name,
                email=email,
                username=username,
                password=password,
                is_email_verified=True,
            )

            response = authenticate(email, password)

            return response
        else:
            user: User = User.objects.filter(email=email,is_deleted=False).latest("date_joined")
            decrypted_password = decrypt(user.encrypted_password)

            response = authenticate(email, decrypted_password)

            return response