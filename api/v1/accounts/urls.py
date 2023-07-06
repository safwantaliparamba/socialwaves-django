from django.urls import re_path

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from . import views


app_name = 'api_v1_accounts'
 
urlpatterns = [
    # base api to check user session and other informations
    re_path(r'^app/$',views.app), 
    # auth
    re_path(r'^sign-up/$',views.signup),
    re_path(r'^sign-in/$',views.login),
    re_path(r'^sign-in-with-google/$',views.google_authentication),
    re_path(r'^sign-out/(?P<session_id>.*)/$',views.sign_out),
    re_path(r'^email/confirm/(?P<token>.*)/$',views.email_confirmation),
    # settings apis
    re_path(r'settings/profile/$', views.settings_public_profile),
    re_path(r'settings/profile/edit/$', views.edit_public_profile),


    #jwt auth routes
    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
