from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .querysets import VideoQuerySet


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_embed_link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Use custom queryset
    objects = VideoQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.filter(is_like=True).count()

    @property
    def dislike_count(self):
        return self.likes.filter(is_like=False).count()

    @property
    def comment_count(self):
        return self.comments.count()




    

