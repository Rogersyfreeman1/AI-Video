# YouTube API Setup Guide

To upload videos directly to YouTube, you need to set up the YouTube Data API. This is a one-time setup.

## Step 1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name it "AI Video System" (or anything you like)
4. Click "Create"

## Step 2: Enable YouTube Data API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click it, then click "Enable"

## Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If asked, configure the consent screen first:
   - User Type: External
   - App name: AI Video System
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue" through the scopes and test users (you can skip these)
4. Back in Credentials, click "Create Credentials" → "OAuth client ID"
5. Application type: **Desktop app**
6. Name: "AI Video Uploader"
7. Click "Create"
8. Click "Download JSON" — save this file as `client_secrets.json` in the AI-Video folder

## Step 4: Configure .env

In your `.env` file, set:
```
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
```

## Step 5: First Upload (OAuth Flow)

The first time you upload, a browser window will open asking you to log in to Google and approve the app. This is normal.

1. Run: `python main.py --topic "Test" --upload`
2. Browser opens → Log in to your Google account
3. Click "Allow" to grant permission
4. The app will save a `token.pickle` file — future uploads won't need the browser

## Privacy Settings

- `private` — Only you can see it (default, safe for testing)
- `unlisted` — Anyone with the link can see it
- `public` — Everyone can see it

Use `--privacy public` when you're ready to publish.

## Troubleshooting

**"Client secrets file not found"**
- Make sure `client_secrets.json` is in the AI-Video folder
- Check the filename matches what's in your `.env`

**"Access blocked"**
- Your OAuth app is in "Testing" mode. Add your Google account as a test user in Google Cloud Console → OAuth consent screen → Test users.

**"Quota exceeded"**
- YouTube API has a daily quota (10,000 units). Each upload costs ~1,600 units. You can upload ~6 videos per day on the free tier. If you need more, request a quota increase from Google.

## No API? No Problem.

Without YouTube API setup, the system still creates videos and saves them locally. You can upload manually via YouTube Studio (youtube.com/upload). The API just automates it.
