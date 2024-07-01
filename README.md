# YouTube Playlist Downloader

A Flask-based web application to download YouTube playlists as audio or video files. This application utilizes the YouTube Data API and `yt-dlp` for downloading content.

<img src="https://github.com/Marti-code/yt-playlist-converter/blob/master/static/weload-desktop.jpg"/>

## Description

This project allows users to input a YouTube playlist URL and download all videos in the playlist as audio or video files. The application fetches playlist information using the YouTube Data API and downloads the content using `yt-dlp`.

## Features

- Fetches YouTube playlist information (title, number of videos, thumbnail).
- Downloads all videos in the playlist as audio or video.
- Zips the downloaded files for easy download.


# Setup

### Prerequisites

- Python 3.9+
- A YouTube Data API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yt-playlist-downloader.git
   cd yt-playlist-downloader
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
3. Create a .env file in the project root directory and add your YouTube Data API key:
   ```bash
   YT_API_KEY="YOUR_YOUTUBE_API_KEY"
4. Run the application:
   ```bash
   python app.py
5. Open web browser:
   http://127.0.0.1:5000


