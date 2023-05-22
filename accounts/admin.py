from django.contrib import admin

from accounts.models import User, ProfileActivity


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email","id",]


@admin.register(ProfileActivity)
class ProfileActivityAdmin(admin.ModelAdmin):
    list_display = ["id","visitor","profile"]