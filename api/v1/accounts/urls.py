from django.urls import re_path

from . import views


app_name = 'api_v1_accounts'

urlpatterns = [
    re_path(r'',views.test),
]