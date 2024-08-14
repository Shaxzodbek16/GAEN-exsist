from django.contrib import admin
from .models import Art, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    _ = ('name', 'created_at', 'description')
    list_display, list_filter, search_fields = _, _, _


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    _ = ('title', 'description', 'is_accepted', 'created_at', 'update_at', 'user')
    list_display, list_filter, search_fields = _, _, _


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    _ = ('art', 'text', 'user', 'created_at')
    list_display, list_filter, search_fields = _, _, _