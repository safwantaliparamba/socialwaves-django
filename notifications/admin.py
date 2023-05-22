from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['title','id','sender','recipient','is_read','title']
    list_filter = ['is_read','date_added']