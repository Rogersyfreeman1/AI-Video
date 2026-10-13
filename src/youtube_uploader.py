"""
YouTube Uploader - Upload videos to YouTube via API
Uses Google YouTube Data API v3 with OAuth.
"""

import os
import json

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

from config import YOUTUBE_CLIENT_SECRETS_FILE


class YouTubeUploader:
    def __init__(self):
        self.youtube = None
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    def authenticate(self):
        """
        Authenticate with YouTube via OAuth.
        Returns True if successful, False otherwise.
        """
        if not YOUTUBE_AVAILABLE:
            print("YouTube API libraries not installed. Run: pip install google-api-python-client google-auth-oauthlib")
            return False

        if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
            print(f"Client secrets file not found: {YOUTUBE_CLIENT_SECRETS_FILE}")
            print("Download it from Google Cloud Console > Credentials > OAuth 2.0 Client ID")
            print("See YOUTUBE_SETUP.md for instructions")
            return False

        credentials = None
        token_file = "token.pickle"

        # Load existing token if available
        if os.path.exists(token_file):
            try:
                with open(token_file, 'rb') as token:
                    credentials = pickle.load(token)
            except:
                credentials = None

        # Refresh or get new credentials
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except:
                    credentials = None

            if not credentials:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        YOUTUBE_CLIENT_SECRETS_FILE, self.scopes)
                    credentials = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Authentication failed: {e}")
                    return False

            # Save credentials
            try:
                with open(token_file, 'wb') as token:
                    pickle.dump(credentials, token)
            except:
                pass

        try:
            self.youtube = build("youtube", "v3", credentials=credentials)
            print("YouTube authentication successful!")
            return True
        except Exception as e:
            print(f"Failed to build YouTube service: {e}")
            return False

    def upload_video(self, video_path, title, description, tags, privacy="private"):
        """
        Upload a video to YouTube.
        Returns video ID if successful, None otherwise.
        privacy: private, unlisted, or public
        """
        if not self.youtube:
            if not self.authenticate():
                print("Cannot upload: authentication failed")
                print(f"Video saved locally at: {video_path}")
                print("Upload manually via YouTube Studio, or set up API credentials")
                return None

        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None

        print(f"Uploading {video_path} to YouTube...")
        print(f"Title: {title}")
        print(f"Privacy: {privacy}")

        try:
            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "27",  # Education
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                }
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = request.execute()
            video_id = response.get("id")
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print(f"Upload successful!")
            print(f"Video URL: {video_url}")
            return video_id

        except Exception as e:
            print(f"Upload failed: {e}")
            print(f"Video saved locally at: {video_path}")
            return None
