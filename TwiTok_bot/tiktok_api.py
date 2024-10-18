import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TikTokAPI:
    def __init__(self, driverPath, tiktokUrl="https://www.tiktok.com/login?lang=fr&redirect_url=https%3A%2F%2Fwww.tiktok.com%2Fupload"):
        """
        Initializes the TikTokAPI instance with the driver path and TikTok URL.

        :param driverPath: Path to the Chrome driver executable.
        :param tiktokUrl: URL for the TikTok login page.
        """
        self.driverPath = driverPath
        self.tiktokUrl = tiktokUrl
        self.driver = None

    def startDriver(self):
        """
        Starts the Chrome driver, opens the TikTok URL, maximizes the window, and sends it to the background.
        """
        service = Service(self.driverPath)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.tiktokUrl)
        self.driver.maximize_window()

    def login(self, username, password, loginChannel):
        """
        Logs in to TikTok using the provided credentials.

        :param username: The TikTok username.
        :param password: The TikTok password.
        :param loginChannel: The login method (Username or Google).
        """

        if loginChannel == 'Username':
            usePhoneEmailOption = self.driver.find_element(By.XPATH, "//div[contains(text(), \"Utiliser téléphone/e-mail/nom d'utilisateur\")]")
            usePhoneEmailOption.click()

            emailLoginOption = self.driver.find_element(By.XPATH, "//a[contains(text(), \"Connexion avec une adresse e-mail ou un nom d'utilisateur\")]")
            emailLoginOption.click()

            usernameInput = self.driver.find_element(By.NAME, "username")
            usernameInput.send_keys(username)

            passwordInput = self.driver.find_element(By.XPATH, "//input[@placeholder='Mot de passe']")
            passwordInput.send_keys(password)

            loginButton = self.driver.find_element(By.XPATH, "//button[@data-e2e='login-button']")
            loginButton.click()

            self.checkCaptcha()

        elif loginChannel == 'Google':
            return
    
    def checkCaptcha(self):
        """
        Checks for a CAPTCHA on the page and waits until the user solves it.
        """
        logging.info("Checking for CAPTCHA...")
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "captcha-verify-container"))
                )
                logging.info("CAPTCHA detected. Please solve it manually.")
                time.sleep(20)
                break
            except:
                logging.info("No CAPTCHA detected or CAPTCHA solved.")
                break

    def uploadVideo(self, videoPath, description):
        """
        Uploads a video to TikTok, adds a description, and posts the video.

        :param videoPath: The path to the video file.
        :param description: The description text for the video.
        """
        try:
            self.driver.get("https://www.tiktok.com/tiktokstudio/upload")
            
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-e2e='select_video_container']"))
            )
            
            videoInput = self.driver.find_element(By.XPATH, "//input[@type='file' and @accept='video/*']")
            videoInput.send_keys(videoPath)
            time.sleep(5)

            descriptionInput = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']")
            descriptionInput.click()
            descriptionInput.clear()
            descriptionInput.send_keys(description)
           
            postButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='post_video_button']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", postButton)
            logging.info(f"Scrolled to element: //button[@data-e2e='post_video_button']")
            postButton.click()
            logging.info("Video posted successfully!")
            
        except Exception as e:
            logging.error(f"Error during video upload: {e}")

    def closeDriver(self):
        """
        Closes the Chrome browser and quits the driver session.
        """
        if self.driver:
            self.driver.quit()