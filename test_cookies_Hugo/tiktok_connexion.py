import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By #pour localiser les elts html (att etc) 
from selenium.webdriver.common.keys import Keys #pour appuyer sur echap 
from selenium.webdriver.support.ui import WebDriverWait #pour attendre qu'une condition soit remplie avant d'executer la tache suivante 
from selenium.webdriver.support import expected_conditions as EC #pour définir ce qu'on attend d'un element avant de poursuivre 
import time
import os 
import pickle #pour les cookies 
import logging #pour suivre l'execution d'un programme 

logging.basicConfig(level=logging.INFO) # on définit le niveau le plus bas de warning pour que la console décrive la situation. En gros la le niveau le plus bas est INFO donc toutes les infos et les choses plus graves que info (bug etc par exemple) seront décritent dans la console 

class tiktok_api : 
    def __init__(self, tiktok_url="https://www.tiktok.com/login/phone-or-email/email"):
        self.tiktok_url = tiktok_url
        self.driver = None
        
    def start_driver(self):
        logging.info("starting undetected Chrome driver")
        # options = uc.ChromeOptions() 
        try: 
            self.driver = uc.Chrome() 
            logging.info(f"Opening Tiktok : {self.tiktok_url}")
            self.driver.get(self.tiktok_url) #load la page rentrée en parametre
            # input("Appuyez sur Entrée pour quitter et fermer le navigateur") #pour laisser ouvert 

        except Exception as e:
            logging.error(f"error while starting driver :{e}")

    # def first_time_login (self) : 


    def login(self): 
        logging.info("first-time login in progress")
        wait = WebDriverWait(self.driver, 10) # executera la suite si elle st executable, sinon attendre jusqu'a 1à secondes qu'elle soit executable 
        time.sleep(2)

        username = input("adresse email :")
        mdp = input ("mot de passe : ")
        try: 
            username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.click()
            logging.info("enter_email zone found and clicked")
        except Exception as e : 
            logging.error(f"enter_email not found, error :{e}")
        username_input.send_keys(username)

        password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mot de passe']")))
        try: 
            password_input.click()
            logging.info("mdp_zone zone found and clicked")
        except Exception as e : 
            logging.error(f"mdp_zone not found, error :{e}")
        password_input.send_keys(mdp)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='login-button']")))
        login_button.click()
        WebDriverWait(self.driver, 15).until(EC.url_contains("tiktok.com"))
        logging.info("Login successful. Saving cookies for future logins.")

        input("Appuyez sur Entrée pour arreter le programme :")
        

        


tiktok_api = tiktok_api() 
tiktok_api.start_driver()
tiktok_api.login() 