from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from pytube import Playlist, YouTube


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

    for video in playlist.videos:
        video.streams.get_highest_resolution().download('downloads/')  # Change the download directory as needed

    return "Download completed!"
