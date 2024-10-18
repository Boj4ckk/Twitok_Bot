import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TikTokAPI:
    def __init__(self, tiktok_url="https://www.tiktok.com/upload"):
        self.tiktok_url = tiktok_url
        self.driver = None
        self.cookie_file = "tiktok_cookies.pkl"  # File to store cookies

    def start_driver(self):
        logging.info("Starting undetected Chrome driver")
        options = uc.ChromeOptions()

        # Stealthy options to avoid detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")

        try:
            self.driver = uc.Chrome(options=options)
            logging.info(f"Opening TikTok: {self.tiktok_url}")
            self.driver.get(self.tiktok_url)
            time.sleep(3)

        except Exception as e:
            logging.error(f"Error while starting driver: {e}")

    def login(self):
        """Log in to TikTok using username and password if cookies are not found."""
        if self.cookies_exist():
            logging.info("Cookies found. Loading cookies to skip login.")
            self.load_cookies()
            self.driver.get(self.tiktok_url)
            time.sleep(3)
        else:
            logging.info("Cookies not found. Performing first-time login.")
            self.perform_first_time_login()

    def cookies_exist(self):
        """Check if the cookie file exists."""
        return os.path.exists(self.cookie_file)

    def save_cookies(self):
        """Save the cookies to a file after login."""
        with open(self.cookie_file, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)
        logging.info("Cookies saved successfully.")

    def load_cookies(self):
        """Load cookies from the file to bypass login."""
        with open(self.cookie_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        logging.info("Cookies loaded successfully.")

    def perform_first_time_login(self):
        """Prompt the user for login credentials and save cookies for future logins."""
        wait = WebDriverWait(self.driver, 10)

        # Click the "Utiliser téléphone/e-mail/nom d'utilisateur"
        self.select_login_option("Utiliser téléphone/e-mail/nom d'utilisateur")

        # Click the email/username login option
        email_login_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), \"Connexion avec une adresse e-mail ou un nom d'utilisateur\")]")
        ))
        email_login_link.click()

        # Ask the user to input their username and password
        username = input("Enter your TikTok username: ")
        password = input("Enter your TikTok password: ")

        # Enter the username and password
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys(username)

        password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mot de passe']")))
        password_input.clear()
        password_input.send_keys(password)

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='login-button']")))
        login_button.click()

        # Wait for successful login and save the cookies
        WebDriverWait(self.driver, 15).until(EC.url_contains("tiktok.com"))
        logging.info("Login successful. Saving cookies for future logins.")
        self.save_cookies()

    def select_login_option(self, option_text):
        """Helper function to select the login option based on the provided text"""
        wait = WebDriverWait(self.driver, 10)
        try:
            option_element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(text(), \"{option_text}\")]")
            ))
            option_element.click()
            time.sleep(2)
            logging.info(f"Selected login option: {option_text}")
        except Exception as e:
            logging.error(f"Could not find login option '{option_text}': {e}")

    def close_driver(self):
        """Close the WebDriver session"""
        if self.driver:
            logging.info("Closing WebDriver session")
            self.driver.quit()
