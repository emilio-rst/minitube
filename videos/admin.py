from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'like_count', 'dislike_count', 'comment_count', 'popularity_score')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'user__username')
    readonly_fields = ('like_count', 'dislike_count', 'comment_count', 'popularity_score')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'youtube_embed_link', 'user')
        }),
        ('Statistics', {
            'fields': ('like_count', 'dislike_count', 'comment_count', 'popularity_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
