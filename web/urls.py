from django.urls import re_path

from web import views


app_name = 'web'

urlpatterns = [
    re_path(r'',views.index),
]