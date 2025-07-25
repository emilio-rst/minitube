from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from videos.models import Video
from .models import Like, Comment
from videos.forms import CommentForm


@login_required
def like_video(request, video_id):
    """Like a video"""
    video = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        like_value = request.POST.get('like') == 'true'
        
        # Update or create like
        like, created = Like.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'is_like': like_value}
        )
        
        if not created:
            # If like already exists, update it
            like.is_like = like_value
            like.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'like_count': video.like_count,
                'dislike_count': video.dislike_count,
                'user_like': like_value
            })
        
        messages.success(request, f'Video {"liked" if like_value else "disliked"} successfully!')
        return redirect('video_detail', video_id=video.id)
    
    return redirect('video_detail', video_id=video.id)


@login_required
def add_comment(request, video_id):
    """Add a comment to a video"""
    video = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Please correct the errors in your comment.')
    
    return redirect('video_detail', video_id=video.id)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (only by the comment author)"""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    video_id = comment.video.id
    comment.delete()
    
    messages.success(request, 'Comment deleted successfully!')
    return redirect('video_detail', video_id=video_id)
