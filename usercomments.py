import os
from googleapiclient.discovery import build
import pandas as pd

# Set your YouTube Data API key
API_KEY = "AIzaSyB7QPpDZMh-lVMFMqFQE1pLshR8r-15joQ"

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_channel_id(username):
    """
    Get the channel ID for a given username.
    """
    request = youtube.channels().list(part="id", forUsername=username)
    response = request.execute()

    if 'items' not in response or not response['items']:
        raise ValueError(f"No channel found for username: {username}")

    return response['items'][0]['id']


def get_video_ids(channel_id):
    """
    Get all video IDs for a given channel.
    """
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids


def get_comments(video_id):
    """
    Get all comments for a given video ID.
    """
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'videoId': video_id,
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'publishedAt': comment['publishedAt'],
                'likeCount': comment['likeCount']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments


def main(username):
    try:
        channel_id = get_channel_id(username)
        print(f"Channel ID: {channel_id}")

        video_ids = get_video_ids(channel_id)
        print(f"Found {len(video_ids)} videos.")

        all_comments = []
        for video_id in video_ids:
            print(f"Fetching comments for video ID: {video_id}")
            comments = get_comments(video_id)
            all_comments.extend(comments)

        # Save comments to a CSV file
        df = pd.DataFrame(all_comments)
        df.to_csv(f"{username}_comments.csv", index=False)
        print(f"Comments saved to {username}_comments.csv")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    username = input("Enter the YouTube username: ")
    main(username)
