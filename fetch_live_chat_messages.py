from googleapiclient.discovery import build
import time
import pandas as pd

# Set your API key
API_KEY = 'AIzaSyB7QPpDZMh-lVMFMqFQE1pLshR8r-15joQ'

# Create the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_live_chat_id(video_id):
    """
    Retrieves the live chat ID for a given YouTube live video.
    Args:
        video_id (str): The YouTube video ID.

    Returns:
        str: The live chat ID if found, otherwise None.
    """
    try:
        response = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        ).execute()

        live_details = response['items'][0].get('liveStreamingDetails', {})
        return live_details.get('activeLiveChatId', None)

    except Exception as e:
        print(f"An error occurred while fetching the live chat ID: {e}")
        return None


def fetch_live_chat_messages(live_chat_id, max_results=500):
    """
    Fetches live chat messages from a YouTube live chat.

    Args:
        live_chat_id (str): The live chat ID.
        max_results (int): Maximum number of messages to retrieve.

    Returns:
        list: A list of dictionaries containing authors and messages.
    """
    messages = []
    try:
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet,authorDetails",
            maxResults=max_results
        )
        response = request.execute()

        for item in response.get('items', []):
            # if item['authorDetails']['displayName'] == "OF":
            author = item['authorDetails']['displayName']
            message = item['snippet']['displayMessage']
            moderator = item['authorDetails']['isChatModerator']
            messages.append({'isChatModerator': moderator,'author': author, 'message': message})

        return messages

    except Exception as e:
        print(f"An error occurred while fetching live chat messages: {e}")
        return []


# Replace with your desired live stream video ID
VIDEO_ID = "-YkHuStR6Mk"

# Main logic
live_chat_id = get_live_chat_id(VIDEO_ID)

if live_chat_id:
    print(f"Live Chat ID: {live_chat_id}")

    # Continuously fetch live chat messages
    while True:
        live_messages = fetch_live_chat_messages(live_chat_id)

        for i, msg in enumerate(live_messages, 1):
            print(f"{i}: {msg['isChatModerator']}: {msg['author']}: {msg['message']}")

        # Wait for a few seconds before fetching new messages
        time.sleep(5)
else:
    print("Could not find a live chat for the given video.")
