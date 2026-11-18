from django.contrib import admin
from .models import Playlist, Video, VideoProgress

# Register your models here.
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'total_videos', 'created_at')
    search_fields = ('title', 'playlist_id', 'user__username')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'playlist',
        'position',
        'duration_seconds'
    )
    search_fields = ('title', 'youtube_video_id')


@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'video',
        'watched_seconds',
        'is_completed',
        'updated_at'
    )
    list_filter = ('is_completed',)
    search_fields = ('user__username', 'video__title')


@property
def progress_percentage(self):

    if self.total_videos == 0:
        return 0

    completed_videos = VideoProgress.objects.filter(
        user=self.user,
        video__playlist=self,
        is_completed=True
    ).count()

    return round(
        (completed_videos / self.total_videos) * 100,
        2
    )
