import os
import json
import logging
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.api.twitch_api import TwitchApi
from src.api.tiktok_api import TiktokApi
from src.config import (
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    DOWNLOAD_FOLDER,
    PROCESSED_FOLDER,
    TIKTOK_USERNAME,
    TIKTOK_PASSWORD,
)

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

# Initialize TikTok and Twitch API instances
twitchApi = TwitchApi(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
tiktokApi = TiktokApi()

# Ensure that necessary directories exist
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# File to store user data
USER_DATA_FILE = "./src/data/users.json"

def loadUsers():
    """
    Load user data from a JSON file.

    :return: A dictionary containing user data, or an empty dictionary if the file doesn't exist.
    """
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def saveUsers(users: dict):
    """
    Save user data to a JSON file.

    :param users: A dictionary containing user data to save.
    """
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)


def addUser(email: str, password: str, tiktokUsername: str, twitchUsername: str):
    """
    Add a new user to the system.

    :param email: The email address of the user.
    :param password: The user's password.
    :param tiktokUsername: The user's TikTok username.
    :param twitchUsername: The user's Twitch username.
    """
    users = loadUsers()
    userId = str(len(users) + 1)
    users[userId] = {
        "email": email,
        "password": generate_password_hash(password),
        "tiktok_username": tiktokUsername,
        "twitch_username": twitchUsername,
    }
    saveUsers(users)


@app.route("/")
def loginPage():
    """
    Route for the login page. Redirects to the dashboard if the user is already logged in.

    :return: Redirect to the appropriate page.
    """
    if session.get("logged_in"):
        return redirect(url_for("dashboardPage"))
    return redirect(url_for("loginPage"))


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    """
    Handle user login.

    :return: Render the login page or redirect to the dashboard on successful login.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users = loadUsers()
        for user in users.values():
            if user["email"] == email and check_password_hash(user["password"], password):
                session["logged_in"] = True
                session["email"] = email
                session["twitch_username"] = user["twitch_username"]
                session["tiktok_username"] = user["tiktok_username"]
                flash("Login successful!", "success")
                return redirect(url_for("dashboardPage"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signupPage():
    """
    Handle user signup.

    :return: Render the signup page or redirect to the login page on successful registration.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        tiktokUsername = request.form.get("tiktok_username")
        twitchUsername = request.form.get("twitch_username")
        users = loadUsers()
        if any(user["email"] == email for user in users.values()):
            flash("Email already registered.", "error")
            return render_template("signup.html")
        addUser(email, password, tiktokUsername, twitchUsername)
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("loginPage"))
    return render_template("signup.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboardPage():
    """
    Dashboard for managing clips and initiating TikTok uploads.

    :return: Render the dashboard page with available clips and errors, if any.
    """
    if not session.get("logged_in"):
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for("loginPage"))

    downloadedVideos = []
    error = None
    if request.method == "POST":
        username = request.form.get("username") or session["twitch_username"]
        minViews = request.form.get("min_views", type=int)
        maxViews = request.form.get("max_views", type=int)
        try:
            userId = twitchApi.getUserId(username)
            if not userId:
                error = "Invalid Twitch username."
            else:
                filters = {}
                if minViews:
                    filters["view_count"] = f">={minViews}"
                if maxViews:
                    filters["view_count"] = f"<={maxViews}"
                clips = twitchApi.getVideos(userId, filters)
                for clip in clips:
                    twitchApi.downloadClipWithAudio(clip, DOWNLOAD_FOLDER)
                    downloadedVideos.append(clip["title"])
        except Exception as exception:
            error = f"Error fetching clips: {exception}"
    return render_template("dashboard.html", videos=downloadedVideos, error=error)


@app.route("/upload_to_tiktok", methods=["POST"])
def uploadToTikTok():
    """
    Upload a video to TikTok.

    :return: Success message or error message if the upload fails.
    """
    try:
        tiktokApi.startDriver()
        if not os.path.exists(tiktokApi.cookiesPath):
            tiktokApi.login(TIKTOK_USERNAME, TIKTOK_PASSWORD)
        videoFile = request.form.get("video_file")
        caption = request.form.get("caption")
        if not videoFile or not caption:
            return "Invalid input.", 400
        tiktokApi.uploadVideo(videoFile, caption)
        return "Video uploaded to TikTok successfully!", 200
    except Exception as exception:
        return f"Error: {exception}", 500
    finally:
        tiktokApi.closeDriver()


@app.route("/logout")
def logoutPage():
    """
    Handle user logout.

    :return: Redirect to the login page after clearing the session.
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("loginPage"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
