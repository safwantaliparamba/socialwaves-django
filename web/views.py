from django.http.request import HttpRequest
from django.http.response import HttpResponse


def index(request: HttpRequest):
    return HttpResponse("<h1 style='text-align:center;'>Socialwaves</h1>")