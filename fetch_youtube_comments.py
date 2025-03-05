from googleapiclient.discovery import build

# Set your API key
API_KEY = 'AIzaSyB7QPpDZMh-lVMFMqFQE1pLshR8r-15joQ'

# Create the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id, max_results=200):
    """
    Fetches comments and their authors from a YouTube video.

    Args:
        video_id (str): The YouTube video ID.
        max_results (int): Maximum number of comments to retrieve.

    Returns:
        list: A list of dictionaries containing comments and author names.
    """
    comments_data = []
    try:
        # Fetch comments using the YouTube Data API
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()

        # Parse response to extract comments and authors
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments_data.append({'author': author, 'comment': comment})

        return comments_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Replace with your desired video ID
VIDEO_ID = "hSojnPyqmyM"

# Get comments and authors
comments_data = get_video_comments(VIDEO_ID)

# Print fetched comments and authors
for i, comment_data in enumerate(comments_data, 1):
    print(f"{i}: {comment_data['author']} said: {comment_data['comment']}")
