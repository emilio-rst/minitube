from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from videos.models import Video


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField()  # True for like, False for dislike
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'video']
        ordering = ['-created_at']

    def __str__(self):
        action = "liked" if self.is_like else "disliked"
        return f"{self.user.username} {action} {self.video.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.video.title}: {self.content[:50]}"


class VideoView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_views')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'video']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.video.title}"
