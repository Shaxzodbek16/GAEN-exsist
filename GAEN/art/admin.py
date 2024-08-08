from django.contrib import admin
from .models import Category, Art, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    _ = ('name', 'created_at', 'description')
    list_display, list_filter, search_fields = _, _, _


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    _ = ('title', 'description', 'category', 'created_at', 'update_at')
    list_display, list_filter, search_fields = _, _, _


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    _ = ('art', 'user', 'text', 'created_at')
    list_display, list_filter, search_fields = _, _, _