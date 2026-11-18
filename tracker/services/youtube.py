
import requests
from django.conf import settings


YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


def get_playlist_details(playlist_id):
    url = f"{YOUTUBE_API_URL}/playlists"

    params = {
        "part": "snippet,contentDetails",
        "id": playlist_id,
        "key": settings.YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    # Check whether the playlist exists
    if not data.get("items"):
        raise ValueError(
            f"Playlist not found. API response: {data}"
        )

    playlist = data["items"][0]

    return {
        "title": playlist["snippet"]["title"],
        "total_videos": playlist["contentDetails"]["itemCount"],
        "playlist_id": playlist_id
    }


def get_playlist_videos(playlist_id):
    url = f"{YOUTUBE_API_URL}/playlistItems"

    videos = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": settings.YOUTUBE_API_KEY
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        for item in data.get("items", []):
            snippet = item["snippet"]

            video_id = item["contentDetails"].get("videoId")

            # Skip deleted or unavailable videos
            if not video_id:
                continue

            thumbnails = snippet.get("thumbnails", {})

            videos.append({
                "youtube_video_id": video_id,
                "title": snippet["title"],
                "position": snippet["position"],
                "thumbnail_url": (
                    thumbnails.get("high", {}).get("url", "")
                )
            })

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    return videos
