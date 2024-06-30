from flask import Blueprint, render_template, request, send_file, jsonify
import yt_dlp
import os
import zipfile
import traceback

views = Blueprint(__name__, "views")

playlist_url = ""

"""
    This module defines the routes for a YouTube playlist downloader web application.
    It includes routes for rendering the home page, loading playlist information, and initiating downloads.

    Routes:
        - /: Home page route.
        - /load: Route for loading playlist information.
        - /download: Route for initiating playlist downloads.
"""


@views.route("/")
def home():
    """
        Render the home page.

        Returns:
            str: The HTML content of the home page.
    """
    return render_template("index.html")


"""
    After user clicked Load button, get the playlist url
    and return playlist title, lenght, image 
"""
@views.route('/load', methods=['POST'])
def load():
    """
        Load playlist information from the provided URL.

        Returns:
            dict: A dictionary containing playlist title, length, and image URL.
    """
    try:
        global playlist_url
        playlist_url = request.form['playlist_url']

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            playlist_title = info_dict.get('title', None)
            playlist_length = len(info_dict.get('entries', []))
            playlist_image = info_dict.get('thumbnails', [{}])[0].get('url', '')

        return jsonify({
            'playlist_title': playlist_title,
            'playlist_length': playlist_length,
            'playlist_image': playlist_image
        })
    except Exception as e:
        print("An error occurred while loading playlist: ", traceback.format_exc())
        return jsonify({'error': 'Failed to load playlist', 'details': traceback.format_exc()}), 500


"""
    After user clicked Download button, get the playlist url,
    create path to the downloads folder,
    create a folder inside of it,
    download the video or music depending on the users choice,
    create a zip file containing the downloaded videos,
    send the zip file to the user for download
"""
@views.route('/download', methods=['POST'])
def download():
    """
        Initiate the download of videos or music from the provided URL.

        Returns:
            file: A zip file containing the downloaded videos or music.
    """
    try:
        global playlist_url
        print(f"Using playlist URL: {playlist_url}")

        source_check = request.form['source_check']
        print(f"Source check value: {source_check}")

        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        print(f"Download path: {download_path}")

        download_folder = os.path.join(download_path, "YouTubeDownloads")
        os.makedirs(download_folder, exist_ok=True)
        print(f"Download folder created at: {download_folder}")

        ydl_opts = {
            'format': 'bestaudio/best' if source_check == "music" else 'best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'quiet': True,
            'no-part': True,  # Prevent creation of .part files
            'retries': 10,  # Increase the number of retries
            'sleep_interval': 5,  # Add sleep interval between retries
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        zipfile_name = os.path.join(download_folder, 'downloaded_videos.zip')
        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for root, _, files in os.walk(download_folder):
                for file in files:
                    if file != 'downloaded_videos.zip':
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))
        print(f"ZIP file created: {zipfile_name}")

        return send_file(zipfile_name, as_attachment=True)
    except Exception as e:
        error_details = traceback.format_exc()
        print("An error occurred while downloading: ", error_details)
        return jsonify({'error': 'Failed to download playlist', 'details': error_details}), 500
