from flask import Blueprint, render_template, request, send_file, jsonify
from googleapiclient.discovery import build
import yt_dlp
import os
import zipfile
import traceback

views = Blueprint(__name__, "views")

YOUTUBE_API_KEY = os.getenv("YT_API_KEY")

playlist_url = ""

@views.route("/")
def home():
    return render_template("index.html")

@views.route('/load', methods=['POST'])
def load():
    try:
        global playlist_url
        playlist_url = request.form['playlist_url']
        playlist_id = playlist_url.split('list=')[-1].split('&')[0] # playlist id without the &feature=shared from the end

        playlist_info = get_playlist_info(YOUTUBE_API_KEY, playlist_id)

        if playlist_info:
            return jsonify({
                'playlist_title': playlist_info['title'],
                'playlist_length': len(playlist_info['video_ids']),
                'playlist_image': playlist_info['image']
            })
        else:
            return jsonify({'error': 'Failed to load playlist'}), 500

    except Exception as e:
        print("An error occurred while loading playlist: ", traceback.format_exc())
        return jsonify({'error': 'Failed to load playlist', 'details': traceback.format_exc()}), 500

@views.route('/download', methods=['POST'])
def download():
    try:
        # playlist_url = request.form['playlist_url']
        global playlist_url
        source_check = request.form['source_check']
        # playlist_url = "https://youtube.com/playlist?list=PLc9lfUMDaofEE4RBWnhHO0HHnuimcpSiw&feature=shared"
        playlist_id = extract_playlist_id(playlist_url)

        playlist_info = get_playlist_info(YOUTUBE_API_KEY, playlist_id)
        if not playlist_info:
            return jsonify({'error': 'Failed to load playlist'}), 500
        

        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        download_folder = os.path.join(download_path, "YouTubeDownloads")
        os.makedirs(download_folder, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best' if source_check == "music" else 'best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'quiet': True,
            'no-part': True,
        }

        video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in playlist_info['video_ids']]

        successful_downloads = []
        failed_downloads = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for video_url in video_urls:
                try:
                    ydl.download([video_url])
                    successful_downloads.append(video_url)
                    print(f"Successfully downloaded: {video_url}")
                except Exception as e:
                    failed_downloads.append(video_url)
                    print(f"Failed to download {video_url}: {e}")

        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")

        zipfile_name = os.path.join(download_folder, 'downloaded_videos.zip')
        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for root, _, files in os.walk(download_folder):
                for file in files:
                    if file != 'downloaded_videos.zip':
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))

        return send_file(zipfile_name, as_attachment=True)
    except Exception as e:
        error_details = traceback.format_exc()
        print("An error occurred while downloading: ", error_details)
        return jsonify({'error': 'Failed to download playlist', 'details': error_details}), 500

def extract_playlist_id(url):
    """
    Extract the playlist ID from a YouTube URL.
    """
    if 'list=' in url:
        return url.split('list=')[-1].split('&')[0]
    return None


def get_playlist_info(api_key, playlist_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    playlist_request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    playlist_response = playlist_request.execute()
    
    playlist_items_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50  # Adjust as needed
    )
    playlist_items_response = playlist_items_request.execute()
    
    if 'items' in playlist_response and len(playlist_response['items']) > 0:
        playlist_info = playlist_response['items'][0]['snippet']
        playlist_title = playlist_info['title']
        playlist_thumbnails = playlist_info['thumbnails']
        playlist_image = playlist_thumbnails['default']['url'] if 'default' in playlist_thumbnails else ''
        
        video_ids = []
        for item in playlist_items_response['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])
        
        return {
            'title': playlist_title,
            'image': playlist_image,
            'video_ids': video_ids
        }
    return None
