import shutil
from flask import Blueprint, render_template, request, send_file
from pytube import Playlist

import os
import zipfile

views = Blueprint(__name__, "views")

playlist_url = ""

@views.route("/")
def home():
    return render_template("index.html")


@views.route('/load', methods=['POST'])
def load():
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
        print("Houston we've got a problem: ", e)


@views.route('/download', methods=['POST'])
def download():
    try:
        global playlist_url
        playlist = Playlist(playlist_url)
        source_check = request.form['source_check']

        desktop_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Create a folder for downloaded videos on the desktop
        download_folder = os.path.join(desktop_path, "YouTubeDownloads")

        # Create a folder for downloaded videos
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

        # Delete the original folder
        shutil.rmtree(download_folder)

        # Send the zip file to the user for download
        return send_file(zipfile_name, as_attachment=True)
    except Exception as e:
        print("Houston we've got a problem: ", e)