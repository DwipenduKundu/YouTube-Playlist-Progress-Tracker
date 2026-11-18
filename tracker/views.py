from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from urllib.parse import urlparse, parse_qs

from .models import Playlist, Video, VideoProgress
from .forms import RegisterForm, PlaylistForm
from .services.youtube import (
    get_playlist_details,
    get_playlist_videos
)


# User Registration
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Your account has been created successfully!'
            )

            return redirect('tracker:dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'tracker/register.html',
        {'form': form}
    )


# User Dashboard
@login_required(login_url='tracker:login')
def dashboard(request):

    playlists = Playlist.objects.filter(
        user=request.user
    )

    playlist_form = PlaylistForm()

    return render(
        request,
        'tracker/dashboard.html',
        {
            'playlists': playlists,
            'playlist_form': playlist_form
        }
    )


# Add YouTube Playlist
@login_required(login_url='tracker:login')
def add_playlist(request):

    if request.method == 'POST':

        form = PlaylistForm(request.POST)

        if form.is_valid():

            playlist_url = form.cleaned_data['playlist_url']

            # Extract playlist ID from URL
            parsed_url = urlparse(playlist_url)
            query_params = parse_qs(parsed_url.query)

            playlist_id = query_params.get('list', [None])[0]

            if not playlist_id:
                messages.error(
                    request,
                    'Could not extract the playlist ID.'
                )
                return redirect('tracker:dashboard')

            try:
                # Fetch playlist details from YouTube
                details = get_playlist_details(playlist_id)

                videos = get_playlist_videos(playlist_id)

                # Save playlist and videos
                with transaction.atomic():

                    playlist, created = Playlist.objects.update_or_create(
                        user=request.user,
                        playlist_id=playlist_id,
                        defaults={
                            'title': details['title'],
                            'playlist_url': playlist_url,
                            'total_videos': details['total_videos']
                        }
                    )

                    for video_data in videos:

                        Video.objects.update_or_create(
                            playlist=playlist,
                            youtube_video_id=video_data['youtube_video_id'],
                            defaults={
                                'title': video_data['title'],
                                'position': video_data['position'],
                                'thumbnail_url': video_data['thumbnail_url']
                            }
                        )

                if created:
                    messages.success(
                        request,
                        'Playlist added successfully!'
                    )
                else:
                    messages.success(
                        request,
                        'Playlist updated successfully!'
                    )

            except ValueError as error:
                messages.error(request, str(error))

            except Exception as error:
                messages.error(
                    request,
                    f'Something went wrong: {error}'
                )

        else:
            messages.error(
                request,
                'Please enter a valid YouTube playlist URL.'
            )

    return redirect('tracker:dashboard')


# Playlist Detail Page
@login_required(login_url='tracker:login')
def playlist_detail(request, playlist_id):

    playlist = get_object_or_404(
        Playlist,
        id=playlist_id,
        user=request.user
    )

    videos = Video.objects.filter(
        playlist=playlist
    )

    completed_videos = VideoProgress.objects.filter(
        user=request.user,
        video__playlist=playlist,
        is_completed=True
    ).values_list('video_id', flat=True)

    completed_video_ids = set(completed_videos)

    for video in videos:
        video.is_completed = video.id in completed_video_ids

    completed_count = len(completed_video_ids)

    return render(
        request,
        'tracker/playlist_detail.html',
        {
            'playlist': playlist,
            'videos': videos,
            'completed_count': completed_count
        }
    )


# Set Video Completion Status
@login_required(login_url='tracker:login')
@require_POST
def mark_video_completed(request):


    video_id = request.POST.get('video_id')
    is_completed = request.POST.get('is_completed')

    if not video_id or is_completed not in ['true', 'false']:

        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid video information.'
            },
            status=400
        )

    video = get_object_or_404(
        Video,
        youtube_video_id=video_id,
        playlist__user=request.user
    )

    progress, created = VideoProgress.objects.get_or_create(
        user=request.user,
        video=video
    )

    # Set the exact completion status
    progress.is_completed = (is_completed == 'true')

    if progress.is_completed:

        if not progress.completed_at:
            progress.completed_at = timezone.now()

    else:

        progress.completed_at = None

    progress.save(
        update_fields=[
            'is_completed',
            'completed_at',
            'updated_at'
        ]
    )

    playlist = video.playlist

    completed_count = VideoProgress.objects.filter(
        user=request.user,
        video__playlist=playlist,
        is_completed=True
    ).count()

    return JsonResponse({
        'success': True,
        'is_completed': progress.is_completed,
        'completed_count': completed_count,
        'total_videos': playlist.total_videos,
        'progress_percentage': playlist.progress_percentage
    })


# Update Live Video Progress
@login_required(login_url='tracker:login')
@require_POST
def update_video_progress(request):

    video_id = request.POST.get('video_id')
    current_time = request.POST.get('current_time')

    if not video_id or current_time is None:

        return JsonResponse(
            {
                'success': False,
                'message': 'Missing video information.'
            },
            status=400
        )

    try:

        current_time = max(0, int(float(current_time)))

    except (ValueError, TypeError):

        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid video position.'
            },
            status=400
        )

    video = get_object_or_404(
        Video,
        youtube_video_id=video_id,
        playlist__user=request.user
    )

    progress, created = VideoProgress.objects.get_or_create(
        user=request.user,
        video=video
    )

    progress.last_position_seconds = current_time

    progress.watched_seconds = max(
        progress.watched_seconds,
        current_time
    )

    progress.save(
        update_fields=[
            'last_position_seconds',
            'watched_seconds',
            'updated_at'
        ]
    )

    return JsonResponse({
        'success': True,
        'last_position_seconds': progress.last_position_seconds
    })
