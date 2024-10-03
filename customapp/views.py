from django.shortcuts import render
import requests
from datetime import datetime
import json


def fetch_youtube_videos(request):
    api_key = 'AIzaSyD2SVUhY3Mjr5iKEAIJKnjZmwFsYyT5K-4'  # Replace with your API key

    search_query = request.GET.get('search_query', '')  # Get the search query from the input field
    queries = [query.strip() for query in search_query.split(',')]  # Split by commas and remove extra spaces

    video_list = []

    for query in queries:
        if query:
            # Create the YouTube search API URL for each query
            url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&maxResults=50&order=date&key={api_key}'
            
            # Make the request to the YouTube API
            response = requests.get(url)
            if response.status_code == 200:
                # Get the response JSON and check for videos
                videos = response.json().get('items', [])
                if not videos:
                    print(f"No videos found for query: {query}")
                
                # Add each video's info to the video_list
                for video in videos:
                    video_id = video['id'].get('videoId')
                    if video_id:  # Filter out non-video results
                        video_info = {
                            'title': video['snippet']['title'],
                            'video_id': video_id,
                            'published_at': video['snippet']['publishedAt'],
                            'thumbnail': video['snippet']['thumbnails']['default']['url'],
                        }
                        video_list.append(video_info)
            else:
                # Print error message if request fails
                print(f"Error fetching videos for query '{query}'. Status code: {response.status_code}")
                print(response.text)  # Print response error details

    if video_list:
        # Remove duplicates based on video_id
        seen_videos = set()
        unique_videos = []
        for video in video_list:
            if video['video_id'] not in seen_videos:
                seen_videos.add(video['video_id'])
                unique_videos.append(video)

        # Sort the video list by published_at in descending order (latest first)
        unique_videos.sort(key=lambda x: datetime.strptime(x['published_at'], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    else:
        unique_videos = []

    # Pass the sorted video list to the template
    return render(request, 'index.html', {'videos': unique_videos})
