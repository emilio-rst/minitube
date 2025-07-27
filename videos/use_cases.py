from django.utils import timezone
from typing import List
import random
from .models import Video


class GetPopularVideosUseCase:
    """
    Use case for retrieving popular videos based on the scoring system.
    This encapsulates the business logic for determining video popularity.
    """
    
    def __init__(self, video_repository=Video.objects):
        """
        Initialize the use case with a video repository.
        Defaults to Django's Video.objects manager.
        """
        self.video_repository = video_repository
    
    def execute(self, limit: int = 5) -> List[Video]:
        """
        Execute the use case to get popular videos.
        
        Args:
            limit: Maximum number of videos to return (default: 5)
            
        Returns:
            List of popular videos sorted by popularity score
        """
        # Get current month videos
        current_month_videos = self._get_current_month_videos()
        
        if current_month_videos.exists():
            return self._get_popular_from_current_month(current_month_videos, limit)
        else:
            return self._get_random_videos(limit)
    
    def _get_current_month_videos(self):
        """Get videos created in the current month with popularity scores calculated."""
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.video_repository.filter(created_at__gte=start_of_month)
    
    def _get_popular_from_current_month(self, current_month_videos, limit: int) -> List[Video]:
        """
        Get popular videos from current month based on popularity scores.
        Uses database-level calculations and sorting for better performance.
        
        Args:
            current_month_videos: QuerySet of current month videos
            limit: Maximum number of videos to return
            
        Returns:
            List of popular videos
        """
        # Use the with_popularity_score queryset method to get videos with calculated scores
        videos_with_scores = current_month_videos.with_popularity_score()
        
        # Order by popularity score (descending) and limit at database level
        popular_videos = list(videos_with_scores.order_by('-popularity_score')[:limit])
        
        # If we have multiple videos and all have the same score, pick random
        if len(popular_videos) > 1:
            first_video = popular_videos[0]
            if all(video.popularity_score == first_video.popularity_score for video in popular_videos):
                # Convert to list and pick random
                all_current_videos = list(current_month_videos)
                popular_videos = random.sample(
                    all_current_videos, 
                    min(limit, len(all_current_videos))
                )
        
        return popular_videos
    
    def _get_random_videos(self, limit: int) -> List[Video]:
        """
        Get random videos when no current month videos exist.
        Uses database-level random selection for better performance.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of random videos
        """
        # Use database-level random selection
        random_videos = list(self.video_repository.order_by('?')[:limit])
        return random_videos 