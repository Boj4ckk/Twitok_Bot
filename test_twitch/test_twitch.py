from dotenv import load_dotenv
import os 

load_dotenv() # charge les infs depuis le .env 

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

import requests

def get_access_token(client_id, client_secret):
    
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Vérifie si la requête a réussi
    token = response.json()["access_token"]
    print("App Access Token obtenu :", token)
    return token

access_token = get_access_token(client_id, client_secret)

def get_clips(channel_name, access_token, client_id):
    # Récupère l'ID de la chaîne Twitch
    def get_channel_id(channel_name):
        url = "https://api.twitch.tv/helix/users"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": client_id
        }
        params = {"login": channel_name}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        if data:
            return data[0]["id"]
        else:
            raise ValueError(f"Channel {channel_name} not found")

    # Récupère les clips associés à une chaîne
    channel_id = get_channel_id(channel_name)
    url = "https://api.twitch.tv/helix/clips"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-ID": client_id
    }
    params = {
        "broadcaster_id": channel_id,
        "first": 5  # Nombre de clips à récupérer
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]

# Exemple d'utilisation
channel_name = "Kamet0"  
clips = get_clips(channel_name, access_token, client_id)
print("Clips récupérés :", clips)

import os

def download_clip(clip, save_path="clips"):
    """Télécharge un clip Twitch."""
    os.makedirs(save_path, exist_ok=True)  # Crée le dossier si nécessaire
    video_url = clip["thumbnail_url"].split("-preview-")[0] + ".mp4"
    file_name = f"{save_path}/{clip['id']}.mp4"
    
    response = requests.get(video_url, stream=True)
    response.raise_for_status()  # Vérifie si la requête a réussi
    
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Clip téléchargé : {file_name}")

# Télécharger les clips récupérés
# for clip in clips:
#     download_clip(clip)


import subprocess

def download_clip_with_audio(clip, save_path="clips"):
    """Télécharge un clip Twitch avec audio via streamlink."""
    os.makedirs(save_path, exist_ok=True)
    video_url = clip["url"]  # Utilisez directement l'URL complète du clip
    file_name = f"{save_path}/{clip['id']}.mp4"
    
    # Utilisation de streamlink pour télécharger le flux avec audio
    command = [
        "streamlink",
        video_url,
        "best",
        "-o",
        file_name
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Clip téléchargé avec succès : {file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement du clip : {clip['id']} ({e})")

for clip in clips:
    download_clip_with_audio(clip)

# for clip in clips:
#     video_url = clip["thumbnail_url"].split("-preview-")[0] + ".mp4"
#     print(f"URL générée : {video_url}")
