import json
from pprint import pprint

from django.http.response import HttpResponse
from django.http.request import HttpRequest

from rest_framework.response import Response

from accounts.models import UserSession
from general.functions import is_valid_uuid, is_ajax


def group_required(group_names):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                if not bool(request.user.groups.filter(name__in=group_names)) | request.user.is_superuser:
                    if is_ajax(request):
                        response_data = {}
                        response_data['status'] = 'false'
                        response_data['stable'] = 'true'
                        response_data['title'] = 'Permission Denied'
                        response_data['message'] = "You have no permission to do this action."
                        # return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        return Response(response_data)
                    else:
                        title= "Permission Denied"
                        return HttpResponse(f'<h1>{title}</h1>')

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def session_required():
    def _method_wrapper(view_method):
        def _arguments_wrapper(request: HttpRequest, *args, **kwargs):
            session_id = request.GET.get("session_id")

            if is_valid_uuid(session_id) and not UserSession.objects.filter(id=session_id, is_active=True).exists():
                    
                if is_ajax(request):
                    response_data = {}
                    response_data['status'] = 'false'
                    response_data['title'] = 'Session Expired'
                    response_data['message'] = "Your session has been expired, please login!"

                    return Response(response_data)
                else:
                    title = "Your session has been expired, please login!"

                    return HttpResponse(f'<h1>{title}</h1>')

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper
