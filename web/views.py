
from pprint import pprint

from django.http.response import HttpResponse
from django.http.request import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def index(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    pprint(request.META["HTTP_USER_AGENT"])
    pprint(request.headers.get("Sec-Ch-Ua-Platform"))

    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    # if request.user_agent.is_mobile:
    #     device_type = "Mobile"
    # if request.user_agent.is_tablet:
    #     device_type = "Tablet"
    # if request.user_agent.is_pc:
    #     device_type = "PC"
    
    # browser_type = request.user_agent.browser.family
    # browser_version = request.user_agent.browser.version_string
    # os_type = request.user_agent.os.family
    # os_version = request.user_agent.os.version_string

    context = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        # "os_type":os_type,
        # "os_version":os_version,
        # # "location_country": location_country,
        # # "location_city": location_city
    }

    # print(context)

    return Response("Socialwaves",status=200)