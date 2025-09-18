from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("phone","email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("phone","email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone","email", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, UserAdmin)
# admin.site.register(User)
admin.site.register(Profile)
