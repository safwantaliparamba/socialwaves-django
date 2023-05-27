from django.contrib import admin

from accounts.models import User, ProfileActivity, UserSession, ChiefProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email","id","name","username","image","is_superuser","is_deleted","is_TFA_activated","is_email_verified"]
    exclude = ["password"]
    actions = ['temp_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    temp_delete.short_description = 'Delete temporarily'


@admin.register(ProfileActivity)
class ProfileActivityAdmin(admin.ModelAdmin):
    list_display = ["id","visitor","profile"]

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user","ip","id","is_active","country","state","location","system"]


@admin.register(ChiefProfile)
class ChiefProfileAdmin(admin.ModelAdmin):
    list_display = ["email","username","profile_type","name"]
    # exclude = ["password"]