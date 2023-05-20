from django.contrib import admin
from django.urls import path,re_path, include
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('chief/', admin.site.urls), #django admin urls

    path('', include('web.urls','web')),
    path('api/v1/accounts/', include('api.v1.accounts.urls','api_v1_accounts')),
    path('api/v1/general/', include('api.v1.general.urls','api_v1_general')),
    path('api/v1/notifications/', include('api.v1.notifications.urls','api_v1_notifications')),
    path('api/v1/posts/', include('api.v1.posts.urls','api_v1_posts')),
    path('api/v1/reports/', include('api.v1.reports.urls','api_v1_reports')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}),
]
