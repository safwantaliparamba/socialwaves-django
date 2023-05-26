from django.urls import re_path

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from . import views


app_name = 'api_v1_accounts'
 
urlpatterns = [
    re_path(r'^app/$',views.app),
    re_path(r'^sign-up/$',views.signup),
    re_path(r'^sign-in/$',views.login),
    re_path(r'^sign-out/(?P<session_id>.*)/$',views.sign_out),
    re_path(r'^email/confirm/(?P<token>.*)/$',views.email_confirmation),

    #jwt auth routes
    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
