from django.contrib import admin
from .models import Like, Comment, VideoView


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at', 'user', 'video')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user', 'video')
    search_fields = ('user__username', 'video__title', 'content')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'viewed_at')
    list_filter = ('viewed_at', 'user', 'video')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'viewed_at'
