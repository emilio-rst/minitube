from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Video
from interactions.models import Like, Comment, VideoView
from datetime import timedelta


class PopularVideosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create videos with different dates and engagement
        self.video1 = Video.objects.create(
            title='Video 1',
            youtube_embed_link='https://www.youtube.com/embed/test1',
            user=self.user,
            created_at=timezone.now() - timedelta(days=1)  # Yesterday
        )
        
        self.video2 = Video.objects.create(
            title='Video 2',
            youtube_embed_link='https://www.youtube.com/embed/test2',
            user=self.user,
            created_at=timezone.now()  # Today
        )
        
        self.video3 = Video.objects.create(
            title='Video 3',
            youtube_embed_link='https://www.youtube.com/embed/test3',
            user=self.user,
            created_at=timezone.now() - timedelta(days=30)  # Last month
        )

    def test_popular_videos_page_loads(self):
        """Test that the popular videos page loads correctly"""
        response = self.client.get(reverse('popular_videos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'videos/popular.html')

    def test_popular_videos_algorithm(self):
        """Test the popularity scoring algorithm"""
        # Add likes, dislikes, and comments to videos
        # Create multiple users for different likes
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        user3 = User.objects.create_user(username='testuser3', password='testpass123')
        
        Like.objects.create(user=self.user, video=self.video1, is_like=True)
        Like.objects.create(user=user2, video=self.video1, is_like=True)  # 2 likes
        Like.objects.create(user=user3, video=self.video1, is_like=False)  # 1 dislike
        Comment.objects.create(user=self.user, video=self.video1, content='Great video!')
        
        # Video 1: 2 likes (20) - 1 dislike (5) + 1 comment (1) + 1 day (100) = 116
        # Video 2: 0 engagement + 0 days = 0
        # Video 3: 0 engagement + 30 days = 3000
        
        # Get popular videos
        response = self.client.get(reverse('popular_videos'))
        videos = response.context['videos']
        
        # Should return videos from current month only (video1 and video2)
        self.assertIn(self.video1, videos)
        self.assertIn(self.video2, videos)
        self.assertNotIn(self.video3, videos)
        
        # Video 1 should be more popular than video 2
        self.assertEqual(videos[0], self.video1)

    def test_popular_videos_same_score_random(self):
        """Test that videos with same popularity score are chosen randomly"""
        # Create multiple videos with same engagement
        for i in range(10):
            video = Video.objects.create(
                title=f'Video {i+4}',
                youtube_embed_link=f'https://www.youtube.com/embed/test{i+4}',
                user=self.user,
                created_at=timezone.now()
            )
            Like.objects.create(user=self.user, video=video, is_like=True)
        
        response = self.client.get(reverse('popular_videos'))
        videos = response.context['videos']
        
        # Should return 5 videos
        self.assertEqual(len(videos), 5)

    def test_popular_videos_no_current_month(self):
        """Test popular videos when no videos exist in current month"""
        # Delete current month videos
        Video.objects.filter(created_at__gte=timezone.now().replace(day=1)).delete()
        
        response = self.client.get(reverse('popular_videos'))
        videos = response.context['videos']
        
        # Should return random videos from all time
        self.assertIn(self.video3, videos)


class UserHistoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        
        # Create videos
        self.video1 = Video.objects.create(
            title='Video 1',
            youtube_embed_link='https://www.youtube.com/embed/test1',
            user=self.user
        )
        
        self.video2 = Video.objects.create(
            title='Video 2',
            youtube_embed_link='https://www.youtube.com/embed/test2',
            user=self.user
        )
        
        self.video3 = Video.objects.create(
            title='Video 3',
            youtube_embed_link='https://www.youtube.com/embed/test3',
            user=self.user
        )

    def test_history_page_requires_login(self):
        """Test that history page requires authentication"""
        response = self.client.get(reverse('user_history'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_history_page_loads(self):
        """Test that the history page loads correctly for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'videos/history.html')

    def test_history_shows_user_videos_only(self):
        """Test that history only shows videos viewed by the current user"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create video views for different users
        VideoView.objects.create(user=self.user, video=self.video1)
        VideoView.objects.create(user=self.user, video=self.video2)
        VideoView.objects.create(user=self.other_user, video=self.video3)
        
        response = self.client.get(reverse('user_history'))
        page_obj = response.context['page_obj']
        
        # Should only show videos viewed by current user
        self.assertEqual(len(page_obj), 2)
        self.assertIn(self.video1, [view.video for view in page_obj])
        self.assertIn(self.video2, [view.video for view in page_obj])
        self.assertNotIn(self.video3, [view.video for view in page_obj])

    def test_history_ordered_newest_first(self):
        """Test that history is ordered from newest to oldest"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create video views with different timestamps
        view1 = VideoView.objects.create(user=self.user, video=self.video1)
        view2 = VideoView.objects.create(user=self.user, video=self.video2)
        
        # Manually set different timestamps
        view1.viewed_at = timezone.now() - timedelta(hours=2)
        view1.save()
        view2.viewed_at = timezone.now() - timedelta(hours=1)
        view2.save()
        
        response = self.client.get(reverse('user_history'))
        page_obj = response.context['page_obj']
        
        # Should be ordered newest first
        self.assertEqual(page_obj[0].video, self.video2)
        self.assertEqual(page_obj[1].video, self.video1)

    def test_history_pagination(self):
        """Test that history is paginated by 10"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create 15 video views
        for i in range(15):
            video = Video.objects.create(
                title=f'Video {i+4}',
                youtube_embed_link=f'https://www.youtube.com/embed/test{i+4}',
                user=self.user
            )
            VideoView.objects.create(user=self.user, video=video)
        
        response = self.client.get(reverse('user_history'))
        page_obj = response.context['page_obj']
        
        # First page should have 10 items
        self.assertEqual(len(page_obj), 10)
        
        # Check second page
        response = self.client.get(reverse('user_history') + '?page=2')
        page_obj = response.context['page_obj']
        
        # Second page should have remaining items
        self.assertEqual(len(page_obj), 5)

    def test_history_empty_for_new_user(self):
        """Test that new users have empty history"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_history'))
        page_obj = response.context['page_obj']
        
        self.assertEqual(len(page_obj), 0)
