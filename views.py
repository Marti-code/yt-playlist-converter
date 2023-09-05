from flask import Blueprint, render_template, request, send_file
from pytube import Playlist

import os
import zipfile

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

        playlist = Playlist(playlist_url)

        playlist_title = playlist.title
        playlist_length = playlist.length
        playlist_image = playlist.videos[0].thumbnail_url

        return {
            'playlist_title': playlist_title,
            'playlist_length': playlist_length,
            'playlist_image': playlist_image
        }
    except Exception as e:
        print("An error occurred while loading playlist: ", e)

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
        playlist = Playlist(playlist_url)
        source_check = request.form['source_check']

        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Create a folder for downloaded videos
        download_folder = os.path.join(download_path, "YouTubeDownloads")
        os.makedirs(download_folder, exist_ok=True)

        for video in playlist.videos:
            if source_check == "music":
                video.streams.get_audio_only().download(download_folder)
            else:
                video.streams.get_highest_resolution().download(download_folder)


        # Create a zip file containing the downloaded videos
        zipfile_name = 'downloaded_videos.zip'
        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for root, _, files in os.walk(download_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))

        # Send the zip file to the user for download
        return send_file(zipfile_name, as_attachment=True)
    except Exception as e:
        print("An error occurred while downloading: ", e)