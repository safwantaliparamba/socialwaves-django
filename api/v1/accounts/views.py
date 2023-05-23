from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from accounts.models import User
from general.http import HttpRequest
from general.functions import is_valid_uuid
from general.encryptions import encrypt, decrypt
from api.v1.accounts.serializers import SignupSerializer
from api.v1.general.functions import generate_serializer_errors, send_email


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: HttpRequest):
    serialized = SignupSerializer(data=request.data)

    if serialized.is_valid():
        user = serialized.save()


        encrypted_user_id = encrypt(user.id)
        context = {
            "user":"there",
            "activation_link":f"http://127.0.0.1:8000/api/v1/accounts/email/confirm/{encrypted_user_id}/"
        }

        verification_email_template = render_to_string('email/account-verification.html',context)

        is_sent = send_email(
            user.email,
            "Activate your Socialwaves account",
            'Confirm your email to continue with Socialwaves',
            verification_email_template
        )

        response_data = {
            "statusCode": 6000,
            "data":{
                "title":"Success",
                "message":"Successfully signed up",
                "is_mailed": is_sent,
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Validation Error Occured",
                "message":generate_serializer_errors(serialized._errors)
            }
        }
     
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([AllowAny])
def email_confirmation(request,token):
    decrypted_user_id = decrypt(token)
    
    if is_valid_uuid(decrypted_user_id) and User.objects.filter(id=decrypted_user_id,is_deleted=False).exists():
        user:User = User.objects.filter(id=decrypted_user_id,is_deleted=False).latest('date_joined')

        user.is_email_verified = True
        user.save()

        return redirect(f"{settings.CLIENT_DOMAIN}/")

    return Response("User not found")