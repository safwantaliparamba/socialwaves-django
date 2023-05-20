from django.http.response import HttpResponse
from django.template.loader import render_to_string

from api.v1.general.functions import send_email


def index(request):
    # template = render_to_string("email/email-verification.html")
    # send_email("safwansafu242090@gmail.com",'Test','Test',template)
    return HttpResponse("<h1 style='text-align:center;'>Socialwaves</h1>")