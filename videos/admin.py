from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'like_count', 'dislike_count', 'comment_count', 'get_popularity_score')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'user__username')
    readonly_fields = ('like_count', 'dislike_count', 'comment_count', 'get_popularity_score')
    date_hierarchy = 'created_at'
    
    def get_popularity_score(self, obj):
        """Get popularity score for admin display"""
        return obj.popularity_score
    get_popularity_score.short_description = 'Popularity Score'
    
    def get_queryset(self, request):
        """Use our custom queryset with popularity scores"""
        # Get the base queryset with all admin filters applied
        queryset = super().get_queryset(request)
        
        # Convert to our custom queryset while preserving filters
        # This is the cleanest way to use Django's built-in filtering
        filtered_ids = queryset.values_list('id', flat=True)
        return Video.objects.filter(id__in=filtered_ids).with_popularity_score()
    
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
