import googleapiclient.discovery
from pytubefix import YouTube
import os

API_KEY = "AIzaSyB7QPpDZMh-lVMFMqFQE1pLshR8r-15joQ"
CHANNEL_ID = "UC554eY5jNUfDq3yDOJYirOQ"
MAX_RESULTS = 100  # YouTube API allows max 50 per request, so we paginate
SAVE_PATH = "audio_downloads/"  # Folder to save audio files

import googleapiclient.discovery
from pytube import YouTube
import os

# Create directory if it doesn't exist
os.makedirs(SAVE_PATH, exist_ok=True)

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)


def get_videos(channel_id, max_results=100):
    video_list = []
    next_page_token = None

    while len(video_list) < max_results:
        response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=min(50, max_results - len(video_list)),
            order="viewCount",
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            if item["id"].get("videoId"):
                video_list.append({
                    "title": item["snippet"]["title"],
                    "videoId": item["id"]["videoId"],
                    "publishedAt": item["snippet"]["publishedAt"]
                })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # No more pages

    return video_list


def download_audio(video_url, save_path=SAVE_PATH):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()  # Get best audio stream
        print(f"Downloading audio: {yt.title}")
        file_path = audio_stream.download(save_path)  # Download as video format (e.g., .mp4)

        # Convert to MP3
        new_file = os.path.splitext(file_path)[0] + ".mp3"
        os.rename(file_path, new_file)
        print(f"Saved as: {new_file}")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")


videos = get_videos(CHANNEL_ID, MAX_RESULTS)

for i, video in enumerate(videos, 1):
    video_url = f"https://www.youtube.com/watch?v={video['videoId']}"
    print(f"{i}. {video['title']} - {video_url}")
    download_audio(video_url)
