from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:video_id>/', views.like_video, name='like_video'),
    path('comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
] 