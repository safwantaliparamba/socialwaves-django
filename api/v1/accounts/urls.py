from django.urls import re_path

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from . import views


app_name = 'api_v1_accounts'
 
urlpatterns = [
    # base api to check user session and other informations
    re_path(r'^app/$',views.app),                                       # GET

    # auth
    re_path(r'^sign-in/$',views.login),                                 # POST
    re_path(r'^sign-up/$',views.signup),                                # POST
    re_path(r'^sign-out/(?P<session_id>.*)/$',views.sign_out),          # POST
    re_path(r'^sign-in-with-google/$',views.google_authentication),     # POST
    re_path(r'^email/confirm/(?P<token>.*)/$',views.email_confirmation),# POST

    # settings apis
    re_path(r'settings/profile/$', views.settings_public_profile),      # GET
    re_path(r'settings/profile/edit/$', views.edit_public_profile),     # POST

    #jwt auth routes
    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
