from flask import Blueprint, render_template, request, jsonify, redirect, send_file, url_for
from pytube import Playlist, YouTube

import os
import zipfile



views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name="Martyna")

# @views.route("/profile/<username>")
# def profile(username):
#     return render_template("index.html", name=username)

# @views.route("/profile")
# def profile():
#     args = request.args
#     name = args.get("name")
#     return render_template("index.html", name=name) #http://127.0.0.1:8000/profile?name=Martyna

@views.route("/profile")
def profile():
    return render_template("profile.html") 

@views.route("/json")
def get_json():
    return jsonify({'name':'Martyna', 'bigbrain':'true'})

@views.route("/go-to-json")
def go_to_json():
    return redirect(url_for("views.get_json"))


# access json from root
# @views.route("/data")
# def get_data():
#     data = request.json
#     return jsonify(data)



@views.route('/download', methods=['POST'])
def download():
    playlist_url = request.form['playlist_url']
    playlist = Playlist(playlist_url)
    download_folder = 'downloads/'

    # Create a folder for downloaded videos
    os.makedirs(download_folder, exist_ok=True)

    for video in playlist.videos:
        video.streams.get_highest_resolution().download(download_folder)

    # Create a zip file containing the downloaded videos
    zipfile_name = 'downloaded_videos.zip'
    with zipfile.ZipFile(zipfile_name, 'w') as zipf:
        for root, _, files in os.walk(download_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_folder))

    # Send the zip file to the user for download
    return send_file(zipfile_name, as_attachment=True)

# def down():
#     try:
#         playlist_url = request.form['playlist_url']
#         ytObject = YouTube(playlist_url)
#         ytVideo = ytObject.streams.get_highest_resolution()
#         ytVideo.download()
#     except:
#         print('YouTube link invalid')
#     print("Success!")
