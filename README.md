TwiTok Bot
==========

Description
-----------
TwiTok Bot is an automated tool designed to help Twitch streamers expand their reach by generating TikTok-ready videos from Twitch clips. By combining Twitch's API for clip extraction and advanced video processing, TwiTok Bot enables content creators to easily produce engaging, short-form content for social media.

Features
--------
- **Clip Extraction**: Automatically extract clips from Twitch based on filters such as title, category, views, duration, and date.
- **Video Processing**: Convert Twitch clips to TikTok's vertical format (9:16) with support for transitions, cropped overlays, and effects.
- **TikTok Integration**: Automatically upload processed videos to TikTok with a user-defined description.
- **Customizable Criteria**: Users can specify their preferences for clip selection and processing.
- **User-Friendly Workflow**: Streamlined processes from clip extraction to TikTok posting.

Setup
-----
### Prerequisites
1. **Python 3.8+**
2. **Google Chrome** installed (for Selenium-based TikTok uploads).
3. **Chromedriver** matching your Chrome version.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Set up Twitch API credentials:
- `TWITCH_CLIENT_ID`: Your Twitch client ID.
- `TWITCH_CLIENT_SECRET`: Your Twitch client secret.

Alternatively, you can edit `src/config.py` to include these directly.

Usage
-----
### Step 1: Authenticate with Twitch
Run the Flask server to initiate authentication:
```bash
python src/app.py
```
Navigate to `http://localhost:5000/auth` to log in and authorize the app. Upon success, you can start fetching clips.

### Step 2: Run the Main Script
```bash
python src/main.py
```
Follow the prompts to:
- Enter your Twitch username.
- Define filters for clip selection (e.g., minimum views, duration).

### Step 3: Review and Process Clips
The selected clips will be downloaded, processed, and saved in the following directories:
- **Downloaded Clips**: `src/edit/twitch_clip/`
- **Processed Clips**: `src/edit/tiktok_clip/`

### Step 4: Upload to TikTok
Processed clips are automatically uploaded to TikTok with the description you provide.

File Structure
--------------
```
project/
├── README.md
├── requirements.txt          # Python dependencies
├── clips_metadata.json       # Saved metadata for Twitch videos
├── src/
│   ├── main.py               # Main orchestrator for the application
│   ├── app.py                # Handles API setup and overall flow
│   ├── config.py             # Centralized configuration
│   ├── api/
│   │   ├── twitch_api.py     # Twitch API interaction
│   │   ├── tiktok_api.py     # TikTok API interaction
│   ├── utils/
│   │   ├── video_utils.py    # Filtering and parsing utilities
│   │   ├── metadata_manager.py # Metadata management
│   ├── edit/
│   │   ├── clip.py           # Clip class and related functions
│   │   ├── video_processor.py # Video processing logic
```

How It Works
------------
1. Authenticate with Twitch.
2. Fetch Twitch clips based on user-defined criteria.
3. Process selected clips into TikTok's vertical format.
4. Upload processed clips to TikTok.

Technologies Used
-----------------
- **Languages**: Python
- **APIs**:
  - Twitch API (clip extraction)
  - TikTok upload via Selenium automation
- **Libraries**:
  - Flask (backend server)
  - MoviePy (video processing)
  - Selenium (automated browser interaction)
  - OpenCV (video analysis)
  - Pillow (image processing)

Testing
-------
### Tests Implemented
1. **Unit Tests**:
   - For Twitch API interactions (clip extraction).
   - For utility functions (e.g., duration parsing, filtering).
   - For video processing modules.
2. **Integration Tests**:
   - End-to-end validation of workflows, from clip extraction to TikTok uploads.
3. **Performance Tests**:
   - Video processing and large-scale clip handling.

Contributors
------------
- **Akil Wael**
- **Aliligali Amir**
- **Hebbinckuys Hugo**
- **Kilito Yazid**

Future Enhancements
-------------------
- Add multi-language support for TikTok captions.
- Integrate AI for automatic clip selection based on user engagement.
- Develop a GUI for more intuitive bot configuration.
