from django.db import models
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import ExtractDay, Now

from .constants import LIKE_WEIGHT, DISLIKE_WEIGHT, COMMENT_WEIGHT, TIME_BONUS_WEIGHT


class VideoQuerySet(models.QuerySet):
    """Custom queryset for Video model with popularity score calculations"""
    
    def with_popularity_score(self):
        """
        Returns a queryset with calculated popularity scores.
        This method can be called on any existing queryset to add popularity score annotations.
        """
        return self.annotate(
            # Count likes (is_like=True)
            annotated_like_count=Count(
                'likes',
                filter=Q(likes__is_like=True),
                distinct=True
            ),
            # Count dislikes (is_like=False)
            annotated_dislike_count=Count(
                'likes',
                filter=Q(likes__is_like=False),
                distinct=True
            ),
            # Count comments
            annotated_comment_count=Count('comments', distinct=True),
            # Calculate days since creation using database functions
            days_since_creation=ExtractDay(Now() - F('created_at')),
            # Calculate popularity score with time bonus
            popularity_score=ExpressionWrapper(
                (F('annotated_like_count') * LIKE_WEIGHT) - (F('annotated_dislike_count') * DISLIKE_WEIGHT) + 
                (F('annotated_comment_count') * COMMENT_WEIGHT) + (F('days_since_creation') * TIME_BONUS_WEIGHT),
                output_field=IntegerField()
            )
        ) 