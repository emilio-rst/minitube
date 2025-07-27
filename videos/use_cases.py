from django.utils import timezone
from typing import List
import random
from .models import Video


class GetPopularVideosUseCase:
    """
    Use case for retrieving popular videos based on the scoring system.
    This encapsulates the business logic for determining video popularity.
    """
    
    def __init__(self, video_repository=None):
        """
        Initialize the use case with a video repository.
        Defaults to Django's Video.objects manager.
        """
        self.video_repository = video_repository or Video.objects
    
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
        """Get videos created in the current month."""
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.video_repository.filter(created_at__gte=start_of_month)
    
    def _get_popular_from_current_month(self, current_month_videos, limit: int) -> List[Video]:
        """
        Get popular videos from current month based on popularity scores.
        
        Args:
            current_month_videos: QuerySet of current month videos
            limit: Maximum number of videos to return
            
        Returns:
            List of popular videos
        """
        # Calculate popularity scores and sort
        videos_with_scores = []
        for video in current_month_videos:
            score = video.popularity_score
            videos_with_scores.append((video, score))
        
        # Sort by popularity score (descending)
        videos_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top videos
        popular_videos = [video for video, score in videos_with_scores[:limit]]
        
        # If all videos have the same score, pick random
        if len(videos_with_scores) > 1:
            first_score = videos_with_scores[0][1]
            if all(score == first_score for _, score in videos_with_scores[:limit]):
                popular_videos = random.sample(
                    list(current_month_videos), 
                    min(limit, current_month_videos.count())
                )
        
        return popular_videos
    
    def _get_random_videos(self, limit: int) -> List[Video]:
        """
        Get random videos when no current month videos exist.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of random videos
        """
        all_videos = list(self.video_repository.all())
        return random.sample(all_videos, min(limit, len(all_videos))) if all_videos else [] 