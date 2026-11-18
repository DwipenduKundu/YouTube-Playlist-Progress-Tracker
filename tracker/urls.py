from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tracker'

urlpatterns = [
    # We will add application URLs here
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Registration
    path('register/', views.register, name='register'),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='tracker/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='tracker:login'
        ),
        name='logout'
    ),

    # Add YouTube Playlist
    path(
        'add-playlist/',
        views.add_playlist,
        name='add_playlist'
    ),

    # Forgot password
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='tracker/password_reset.html',
            email_template_name='tracker/password_reset_email.html',
            subject_template_name='tracker/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),

    # Email sent confirmation
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='tracker/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Set new password
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='tracker/password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),

    # Password reset completed
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='tracker/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Playlist Detail
    path(
        'playlist/<int:playlist_id>/',
        views.playlist_detail,
        name='playlist_detail'
    ),
    path(
        'mark-video-completed/',
        views.mark_video_completed,
        name='mark_video_completed'
    ),
    path(
        'update-video-progress/',
        views.update_video_progress,
        name='update_video_progress'
    ),
]


