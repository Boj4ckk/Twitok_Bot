
# TwiTok Bot

## Description
**TwiTok Bot** is a web application designed to help Twitch streamers create TikTok-ready videos from their Twitch clips. By combining Twitch's API for clip extraction, advanced video processing, and a user-friendly dashboard, TwiTok Bot simplifies the content creation process for streamers looking to expand their audience on TikTok.

---

## Features
- **User Authentication**:
  - Secure sign-up and login functionality with user-specific settings.
- **Clip Extraction**:
  - Extract Twitch clips based on:
    - Minimum views
    - Duration
    - Date range
  - Store metadata for downloaded clips.
- **Video Processing**:
  - Convert Twitch clips into TikTok's vertical format (9:16).
  - Add custom overlays, crop videos, and edit for TikTok compatibility.
- **Dashboard**:
  - View and manage downloaded clips with metadata:
    - Title, views, duration, and URLs.
  - Add descriptions for each video directly on the dashboard.
- **Static Styling**:
  - Modern and responsive interface using `style.css`.
- **Testing**:
  - Unit and integration tests for API interactions and video processing.

---

## Setup

### **Prerequisites**
1. **Python 3.8+**
2. **Google Chrome** installed.
3. **Chromedriver** installed and compatible with your Chrome version (managed automatically via `webdriver-manager`).

### **Install Dependencies**
Run the following command to install all required dependencies:
```bash
pip install -r requirements.txt
```

### **Environment Variables**
Configure the following environment variables:
- `TWITCH_CLIENT_ID`: Your Twitch app's client ID.
- `TWITCH_CLIENT_SECRET`: Your Twitch app's client secret.
- `TIKTOK_USERNAME`: TikTok username for uploads (stored for login automation).
- `TIKTOK_PASSWORD`: TikTok password for uploads (stored for login automation).

Alternatively, you can configure these values in `src/config.py`.

---

## Usage

### **Step 1: Run the Application**
Start the Flask server to launch the TwiTok Bot:
```bash
python src/app.py
```
The application will be accessible at `http://localhost:5000`.

---

### **Step 2: Workflow**

#### **1. Sign-Up or Login**
- Create an account with:
  - Email
  - Password
  - Twitch username
  - TikTok username
- Log in to access the dashboard.

#### **2. Extract Clips**
- On the **Dashboard**:
  - Enter Twitch username.
  - Set filters (views, duration, date range).
  - Click **Download** to fetch clips.
- The downloaded clips are displayed in a table with their:
  - Title, views, duration, URL, and editable description.

#### **3. Add Descriptions**
- Add custom descriptions for each video in the provided input fields.

#### **4. Upload to TikTok**
- Click **Upload All Videos** to process and upload the clips.
- **Note**: Upload functionality is currently under development due to ChromeDriver integration issues.

---

## File Structure
```
TwiTok_Bot/
├── README.md                     # Project documentation
├── requirements.txt              # List of dependencies
├── src/                          # Main source code
│   ├── app.py                    # Entry point for Flask web server
│   ├── main.py                   # Orchestrates workflows
│   ├── config.py                 # Configuration for APIs and file paths
│   ├── api/                      # API integrations
│   │   ├── tiktok_api.py         # TikTok upload automation (Selenium)
│   │   ├── twitch_api.py         # Twitch clip extraction
│   ├── data/                     # Metadata and user data
│   │   ├── clips_metadata.json   # Saved Twitch clip metadata
│   │   ├── users.json            # User data
│   ├── edit/                     # Video processing modules
│   │   ├── clip.py               # Clip class and utilities
│   │   ├── video_processor.py    # Video editing and formatting logic
│   │   ├── transition_manager.py # Transition effects
│   │   ├── tiktok_clip/          # Processed TikTok clips
│   │   ├── twitch_clip/          # Downloaded Twitch clips
│   ├── static/                   # Static files (CSS)
│   │   ├── style.css             # Main stylesheet
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base layout
│   │   ├── dashboard.html        # Dashboard page
│   │   ├── login.html            # Login page
│   │   ├── signup.html           # Sign-up page
│   ├── tests/                    # Test modules
│   │   ├── test_tiktok_api.py    # Unit tests for TikTok API
│   │   ├── test_twitch_api.py    # Unit tests for Twitch API
│   │   ├── test_video_processor.py # Tests for video processing
│   ├── utils/                    # Utility scripts
│   │   ├── logger.py             # Logging utility
│   │   ├── metadata_manager.py   # Manages metadata for clips
│   │   ├── video_utils.py        # Video filtering utilities
```

---

## Technologies Used
- **Languages**: Python
- **Backend**: Flask
- **Video Processing**: MoviePy, OpenCV, Pillow
- **Browser Automation**: Selenium, WebDriver Manager
- **Streaming Utility**: Streamlink
- **Password Security**: Werkzeug

---

## Testing
### **Tests Implemented**
1. **Unit Tests**:
   - Twitch API: Clip extraction and filtering.
   - Video Processing: Cropping, formatting, and metadata parsing.
2. **Integration Tests**:
   - Full workflow testing: From clip extraction to upload.
3. **Performance Tests**:
   - Processing multiple clips efficiently.

---

## Contributors
- **Akil Wael**
- **Aliligali Amir**
- **Hebbinckuys Hugo**
- **Kilito Yazid**

---

## Known Issues
1. **TikTok Upload Automation**:
   - Currently facing compatibility issues with ChromeDriver for Selenium automation.
2. **Future Enhancements**:
   - Add AI-based clip selection for better engagement.
   - Optimize video processing performance.
   - Develop a GUI for improved usability.

---