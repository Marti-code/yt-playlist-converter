from flask import Blueprint, render_template, request, jsonify, redirect, send_file, url_for
from pytube import Playlist, YouTube

import os
import youtube_dl
import zipfile


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name="Martyna")


@views.route('/download', methods=['POST'])
def download():
    try:
#     playlist_url = request.form['playlist_url']
        playlist_url = "https://www.youtube.com/watch?v=dLixMzBw2j8"
        print(playlist_url)
        ytObject = YouTube(playlist_url)
        print(ytObject)
        ytVideo = ytObject.streams.get_highest_resolution()
        print(ytVideo)
        ytVideo.download('downloads/')
        print("video downloaded")
    except Exception as e:
        print("Error:", e)
    print("Success!")




# def download():
#     playlist_url = request.form['playlist_url']
#     # Extract playlist ID from URL (you need to implement this)
#     playlist_id = "PLc9lfUMDaofFt7J8fSt1qpRXXeqPF8J1a"

#     ydl_opts = {
#         'format': 'best',
#         'outtmpl': 'downloads/%(title)s.%(ext)s',
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download(['https://www.youtube.com/playlist?list=' + playlist_id])

#     return "Download completed!"







# def download():
#     playlist_url = request.form['playlist_url']
#     playlist = Playlist(playlist_url)
#     download_folder = 'downloads/'

#     # Create a folder for downloaded videos
#     os.makedirs(download_folder, exist_ok=True)

#     for video in playlist.videos:
#         video.streams.get_highest_resolution().download(download_folder)

#     # Create a zip file containing the downloaded videos
#     zipfile_name = 'downloaded_videos.zip'
#     with zipfile.ZipFile(zipfile_name, 'w') as zipf:
#         for root, _, files in os.walk(download_folder):
#             for file in files:
#                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))

#     # Send the zip file to the user for download
#     return send_file(zipfile_name, as_attachment=True)