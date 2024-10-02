from django.shortcuts import render
import requests
from datetime import datetime
import json


def fetch_youtube_videos(request):
    api_key = 'AIzaSyDtNwJ5MW428dyX9AGEfGUiHvYuBpsny9w'  # Replace with your API key

    search_query = request.GET.get('search_query', '')  # Get the search query from the input field
    queries = [query.strip() for query in search_query.split(',')]  # Split by commas and remove extra spaces

    video_list = []

    for query in queries:
        if query:
            # Create the YouTube search API URL for each query
            url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults=50&order=date&key={api_key}'
            response = requests.get(url)
            videos = response.json().get('items', [])

            # Add each video's info to the video_list
            for video in videos:
                video_id = video['id'].get('videoId')
                if video_id:  # Filter out playlists and channels
                    video_info = {
                        'title': video['snippet']['title'],
                        'video_id': video_id,
                        'published_at': video['snippet']['publishedAt'],
                        'thumbnail': video['snippet']['thumbnails']['default']['url'],
                    }
                    video_list.append(video_info)

    # Remove duplicates based on video_id
    video_list = [dict(t) for t in {tuple(d.items()) for d in video_list}]

    # Sort the video list by published_at in descending order (latest first)
    video_list.sort(key=lambda x: datetime.strptime(x['published_at'], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)

    # Pass the sorted video list to the template
    return render(request, 'index.html', {'videos': video_list})



