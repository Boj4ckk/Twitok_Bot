# src/api/tiktok_api.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import pickle

class TiktokApi:
    """
    Automates TikTok video uploads using Selenium.
    """

    def __init__(self, cookiesPath="./tiktok_cookies.pkl"):
        """
        Initialize TikTokAPI instance with Selenium WebDriver.

        :param driverPath: Path to ChromeDriver executable.
        :param cookiesPath: Path to saved TikTok cookies for authentication.
        """
        self.cookiesPath = cookiesPath
        self.driver = None

    def startDriver(self):
        """
        Start the Selenium WebDriver and open TikTok login page.
        """
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()


    def login(self, username, password):
        """
        Log in to TikTok and save cookies for reuse.

        :param username: TikTok username or email.
        :param password: TikTok password.
        """
        self.driver.get("https://www.tiktok.com/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='login-button']"))
        ).click()

        # Handle CAPTCHA manually if it appears
        time.sleep(15)

        # Save cookies for future use
        with open(self.cookiesPath, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        logging.info("Cookies saved for future sessions.")

    def uploadVideo(self, videoPath, description):
        """
        Upload a video to TikTok with a description.

        :param videoPath: Path to the video file.
        :param description: Description text for the video.
        """
        self.driver.get("https://www.tiktok.com/upload")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        ).send_keys(videoPath)

        time.sleep(5)  # Allow video upload to process

        descriptionInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        descriptionInput.clear()
        descriptionInput.send_keys(description)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='post-button']"))
        ).click()
        logging.info(f"Video {videoPath} uploaded with description: {description}")

    def closeDriver(self):
        """
        Close the Selenium WebDriver.
        """
        if self.driver:
            self.driver.quit()
