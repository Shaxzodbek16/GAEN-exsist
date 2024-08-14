from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    _ = ('first_name', 'username', 'country', 'is_active', 'is_staff', 'is_verified', 'date_joined', 'last_login', )
    list_display, list_filter, search_fields = _, _, _
