from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import random
from .models import Video
from .forms import VideoUploadForm
from interactions.models import VideoView
from .use_cases import GetPopularVideosUseCase
from .constants import HOME_VIDEOS_LIMIT, POPULAR_VIDEOS_LIMIT, HISTORY_PAGINATION_PER_PAGE


def home(request):
    """Home page with random videos"""
    videos = list(Video.objects.all())
    if videos:
        # Shuffle videos for random display
        random.shuffle(videos)
        videos = videos[:HOME_VIDEOS_LIMIT]  # Show max videos based on constant
    
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
    """Show the most popular videos based on the scoring system"""
    use_case = GetPopularVideosUseCase()
    popular_videos = use_case.execute(limit=POPULAR_VIDEOS_LIMIT)
    
    return render(request, 'videos/popular.html', {'videos': popular_videos})


@login_required
def user_history(request):
    """Show user's video viewing history"""
    video_views = VideoView.objects.filter(user=request.user).select_related('video')
    
    # Paginate based on constant
    paginator = Paginator(video_views, HISTORY_PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'videos/history.html', {'page_obj': page_obj})
