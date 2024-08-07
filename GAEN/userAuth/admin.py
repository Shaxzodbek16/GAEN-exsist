from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    _ = ('email', 'first_name', 'username', 'country', 'is_active', 'is_staff', 'created_at')
    list_display, list_filter, search_fields = _, _, _
