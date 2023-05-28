from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['title','id','sender','recipient','is_read','title']
    list_filter = ['is_read','date_added']
    actions = ['temp_delete','undo_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'