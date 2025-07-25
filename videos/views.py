from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
import random
from datetime import datetime, timedelta
from .models import Video
from .forms import VideoUploadForm
from interactions.models import VideoView


def home(request):
    """Home page with random videos"""
    videos = list(Video.objects.all())
    if videos:
        # Shuffle videos for random display
        random.shuffle(videos)
        videos = videos[:12]  # Show max 12 videos
    
    return render(request, 'videos/home.html', {'videos': videos})


def video_detail(request, video_id):
    """Video detail page with embed, likes, dislikes, and comments"""
    video = get_object_or_404(Video, id=video_id)
    
    # Record view if user is authenticated
    if request.user.is_authenticated:
        VideoView.objects.get_or_create(user=request.user, video=video)
    
    # Get user's like/dislike status
    user_like = None
    if request.user.is_authenticated:
        try:
            user_like = video.likes.get(user=request.user)
        except:
            pass
    
    return render(request, 'videos/video_detail.html', {
        'video': video,
        'user_like': user_like
    })


@login_required
def upload_video(request):
    """Upload a new video"""
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('video_detail', video_id=video.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VideoUploadForm()
    
    return render(request, 'videos/upload.html', {'form': form})


def popular_videos(request):
    """Show the 5 most popular videos based on the scoring system"""
    # Get current month videos
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    current_month_videos = Video.objects.filter(created_at__gte=start_of_month)
    
    if current_month_videos.exists():
        # Calculate popularity scores and sort
        videos_with_scores = []
        for video in current_month_videos:
            score = video.popularity_score
            videos_with_scores.append((video, score))
        
        # Sort by popularity score (descending)
        videos_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 5 videos
        popular_videos = [video for video, score in videos_with_scores[:5]]
        
        # If all videos have the same score, pick 5 random
        if len(videos_with_scores) > 1:
            first_score = videos_with_scores[0][1]
            if all(score == first_score for _, score in videos_with_scores[:5]):
                popular_videos = random.sample(list(current_month_videos), min(5, current_month_videos.count()))
    else:
        # No videos this month, pick 5 random from all videos
        all_videos = list(Video.objects.all())
        popular_videos = random.sample(all_videos, min(5, len(all_videos))) if all_videos else []
    
    return render(request, 'videos/popular.html', {'videos': popular_videos})


@login_required
def user_history(request):
    """Show user's video viewing history"""
    video_views = VideoView.objects.filter(user=request.user).select_related('video')
    
    # Paginate by 10
    paginator = Paginator(video_views, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'videos/history.html', {'page_obj': page_obj})
