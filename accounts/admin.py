from django.contrib import admin

from accounts.models import User, ProfileActivity, UserSession, ChiefProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email","name","username","image","is_superuser","is_deleted","is_email_verified"]
    exclude = ["password"]
    actions = ['temp_delete','undo_delete']

    def temp_delete(self, request, queryset):
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects temporarily deleted.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'


@admin.register(ProfileActivity)
class ProfileActivityAdmin(admin.ModelAdmin):
    list_display = ["id","visitor","profile"]

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user","ip","id","is_active","is_main","browser","last_active","last_login"]

    actions = ['temp_delete','undo_delete']
    # exclude = ["password"]
    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects temporarily deleted.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'


@admin.register(ChiefProfile)
class ChiefProfileAdmin(admin.ModelAdmin):
    list_display = ["email","username","profile_type","name"]
    actions = ['temp_delete','undo_delete']
    # exclude = ["password"]
    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects temporarily deleted.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'