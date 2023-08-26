from flask import Blueprint, render_template, request, jsonify, redirect, send_file, url_for
from pytube import Playlist, YouTube

import os
import zipfile


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name="Marti")


@views.route('/download', methods=['POST'])
def download():
    try:
        playlist_url = request.form['playlist_url']
        playlist = Playlist(playlist_url)
        source_check = request.form['source_check']
        download_folder = 'downloads/'

        playlist_title = playlist.title
        playlist_length = playlist.length


        # Create a folder for downloaded videos
        os.makedirs(download_folder, exist_ok=True)

        for video in playlist.videos:
            if source_check == "music":
                video.streams.get_audio_only().download(download_folder)
                vid_title = video.title
                thumnail = video.thumbnail_url
            else:
                video.streams.get_highest_resolution().download(download_folder)
                # video.streams.get_by_resolution("720p") #only if done individually
            # render_template("profile.html", name=vid_title)

        # Create a zip file containing the downloaded videos
        zipfile_name = 'downloaded_videos.zip'
        with zipfile.ZipFile(zipfile_name, 'w') as zipf:
            for root, _, files in os.walk(download_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))

        # Send the zip file to the user for download
        return send_file(zipfile_name, as_attachment=True)
    except Exception as e:
        print("Houston we've got a problem: ", e)
