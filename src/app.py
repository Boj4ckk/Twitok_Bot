import os
import json
import logging
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.api.twitch_api import TwitchApi
from src.api.tiktok_api import TiktokApi
# from src.utils.metadata_manager import MetadataManager
from src.config import (
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    DOWNLOAD_FOLDER,
    PROCESSED_FOLDER,
    METADATA_FILE,
    TIKTOK_USERNAME,
    TIKTOK_PASSWORD,
)

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize TikTok and Twitch APIs
twitch_api = TwitchApi(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
tiktok_api = TiktokApi()

# Ensure download directories exist
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# User Management
USER_DATA_FILE = "./src/metadata/users.json"


def load_users():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


def add_user(email, password, tiktok_username, twitch_username):
    users = load_users()
    user_id = str(len(users) + 1)
    users[user_id] = {
        "email": email,
        "password": generate_password_hash(password),
        "tiktok_username": tiktok_username,
        "twitch_username": twitch_username,
    }
    save_users(users)


@app.route("/")
def login_page():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users = load_users()
        for user in users.values():
            if user["email"] == email and check_password_hash(user["password"], password):
                session["logged_in"] = True
                session["email"] = email
                session["twitch_username"] = user["twitch_username"]
                session["tiktok_username"] = user["tiktok_username"]
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        tiktok_username = request.form.get("tiktok_username")
        twitch_username = request.form.get("twitch_username")
        users = load_users()
        if any(user["email"] == email for user in users.values()):
            flash("Email already registered.", "error")
            return render_template("signup.html")
        add_user(email, password, tiktok_username, twitch_username)
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for("login"))

    videos_downloaded = []
    error = None
    if request.method == "POST":
        username = request.form.get("username") or session["twitch_username"]
        min_views = request.form.get("min_views", type=int)
        max_views = request.form.get("max_views", type=int)
        try:
            user_id = twitch_api.getUserId(username)
            if not user_id:
                error = "Invalid Twitch username."
            else:
                filters = {}
                if min_views:
                    filters["view_count"] = f">={min_views}"
                if max_views:
                    filters["view_count"] = f"<={max_views}"
                clips = twitch_api.getVideos(user_id, filters)
                for clip in clips:
                    twitch_api.downloadClipWithAudio(clip, DOWNLOAD_FOLDER)
                    # MetadataManager.saveMetadata([clip], METADATA_FILE)
                    videos_downloaded.append(clip["title"])
        except Exception as e:
            error = f"Error fetching clips: {e}"
    return render_template("dashboard.html", videos=videos_downloaded, error=error)


@app.route("/upload_to_tiktok", methods=["POST"])
def upload_to_tiktok():
    try:
        tiktok_api.startDriver()
        if not os.path.exists(tiktok_api.cookiesPath):
            tiktok_api.login(TIKTOK_USERNAME, TIKTOK_PASSWORD)
        video_file = request.form.get("video_file")
        caption = request.form.get("caption")
        if not video_file or not caption:
            return "Invalid input.", 400
        tiktok_api.uploadVideo(video_file, caption)
        return "Video uploaded to TikTok successfully!", 200
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        tiktok_api.closeDriver()


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
