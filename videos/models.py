from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_embed_link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def popularity_score(self):
        """Calculate popularity score based on the rules"""
        likes = self.like_count * 10
        dislikes = self.dislike_count * 5
        comments = self.comment_count * 1
        
        # Time bonus: 100 points per day since creation
        days_since_creation = (timezone.now() - self.created_at).days
        time_bonus = days_since_creation * 100
        
        return likes - dislikes + comments + time_bonus
