from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import os
import undetected_chromedriver as uc

class TiktokApiManager:
    """
    Initializes a video clip with details such as ID, title, duration, and more.

    :param video: the video edited to post on tiktok.
    :param videoMetaData: all the metadata to post with the video (hashtags, description, etc.).
    """

    def __init__(self, video, videoMetaData):
        self.video = video
        self.videoMetaData = videoMetaData
        self.driver = uc.Chrome() # Passer headless=False pour voir ce qui se passe
        self.cookieFile = "cookie.pkl"

    def tiktok_login(self):
        """
        Logs in to TikTok using Google OAuth via Selenium, but waits for the user to enter the credentials manually.
        Saves cookies after successful login.
        """

        # Accéder à la page de connexion Google pour TikTok
        self.driver.get("https://accounts.google.com/v3/signin/identifier?platform=google&client_id=1096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps.googleusercontent.com&response_type=token&redirect_uri=https%3A%2F%2Fwww.tiktok.com%2Flogin%2F&state=%7B%22client_id%22%3A%221096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps.googleusercontent.com%22%2C%22network%22%3A%22google%22%2C%22display%22%3A%22popup%22%2C%22callback%22%3A%22_hellojs_11hikueo%22%2C%22state%22%3A%22%22%2C%22redirect_uri%22%3A%22https%3A%2F%2Fwww.tiktok.com%2Flogin%2F%22%2C%22scope%22%3A%22basic%22%7D&scope=openid%20profile&prompt=consent&service=lso&o2v=2&ddm=1&flowName=GeneralOAuthFlow&continue=https%3A%2F%2Faccounts.google.com%2Fsignin%2Foauth%2Fconsent%3Fauthuser%3Dunknown%26part%3DAJi8hAO2OnfkogPTxDXsid23Hukl5eL5yyVoxeOKzQp--ZaGcTIdtPYw1EyitiSRzr1trhc5d3PSRqcnUsnBSkzu1DaNsMgNCGZ04WEqBZMRR6CAJk-iZIN5W18cU7QyHkbovZWWw5AzMmRl_XB1H-IO07TqXn3jUu7K1yWNvqm3N3CilnhEve5h4l_aj5fYfD8ArPJQPtOP0gJMRcPL8V462w-Chu9CTQZLg3JXIDz7KGdvVvsNN2jMw1IM6jw0C5k-0x77U_zw1TGOhaS1-l3KbV6YIHn1HEnzgCi2XOTH0130lSvHZfei3Rhu4QEovWDxWQRSsKI-j8L7B2i2m6lC4ZcjV8i1q_2nITHscvpB6pYFyCkYYh7XzTXSpcdlqLf7hYkFASl91zFW5ubAP4gLfIbLl1jRKhFQtkyjw1QQFZAhe85CtZV2a_NCW9CcUNG-Y8wedtChIVX3nldU0ujEm9i4S5zEQA%26flowName%3DGeneralOAuthFlow%26as%3DS1461703116%253A1728500997217796%26client_id%3D1096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps.googleusercontent.com%23")

        # Attendre que l'utilisateur entre son email manuellement
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//*[@type="password"]'))  # Assure-toi que le champ mot de passe est apparu
        )
        print("L'utilisateur a entré l'email et le mot de passe.")

        # Attendre que l'utilisateur complète le processus d'authentification et soit redirigé vers la page principale de TikTok
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Accueil")]'))  # Un élément spécifique après la connexion
        )
        print("L'utilisateur s'est connecté avec succès.")

        # Sauvegarder les cookies après connexion
        with open(self.cookieFile, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        print("Cookies sauvegardés après connexion.")

    def load_cookies(self):
        if os.path.exists(self.cookieFile):
            print("Chargement des cookies...")
            with open(self.cookieFile, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    # Vérifie si le cookie contient un domaine et s'il est différent du domaine actuel
                    if 'domain' in cookie:
                        # Assure-toi que le domaine du cookie correspond à celui du site actuel
                        current_domain = self.driver.current_url.split('/')[2]  # Obtient le domaine actuel
                        cookie['domain'] = current_domain  # Modifie le domaine du cookie

                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"Erreur lors de l'ajout du cookie : {e}")
            return True
        return False

