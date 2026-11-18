from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Playlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='playlists'
    )

    title = models.CharField(max_length=255)

    playlist_id = models.CharField(max_length=100)

    playlist_url = models.URLField()

    total_videos = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'playlist_id'],
                name='unique_user_playlist'
            )
        ]

    def __str__(self):
        return self.title
    
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


class Video(models.Model):

    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='videos'
    )

    youtube_video_id = models.CharField(max_length=100)

    title = models.CharField(max_length=255)

    position = models.PositiveIntegerField()

    duration_seconds = models.PositiveIntegerField(default=0)

    thumbnail_url = models.URLField(blank=True)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['playlist', 'youtube_video_id'],
                name='unique_video_in_playlist'
            )
        ]

    def __str__(self):
        return self.title


class VideoProgress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='video_progress'
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    watched_seconds = models.PositiveIntegerField(default=0)

    last_position_seconds = models.PositiveIntegerField(default=0)

    is_completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'video'],
                name='unique_user_video_progress'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
