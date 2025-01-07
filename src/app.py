import os
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash,  send_file, make_response
import json
import flask
from werkzeug.security import generate_password_hash, check_password_hash
# from test_twitch.test_twitch import get_access_token, get_clips, download_clip_with_audio
import requests
import os
import shutil
import signal 
import subprocess, sys
import time
import api.tiktok_api


app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Remplacez par une clé secrète

# Le chemin vers le fichier JSON pour stocker les utilisateurs
USER_DATA_FILE = "Twitok_Bot\\src\\metadata\\users.json"

# Fonction pour charger les utilisateurs depuis le fichier JSON
def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            data = f.read()
            if not data:  # Si le fichier est vide, retournez un dictionnaire vide
                return {}
            return json.loads(data)  # Charge les données JSON si elles sont présentes
    except json.JSONDecodeError:
        print("Erreur de formatage JSON : Le fichier est corrompu.")
        return {}  # Retourne un dictionnaire vide en cas d'erreur de format
    except FileNotFoundError:
        return {}  # Retourne un dictionnaire vide si le fichier n'existe pas

# Fonction pour sauvegarder les utilisateurs dans le fichier JSON
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Fonction pour ajouter un utilisateur
def add_user(email, password, tiktok_username, twitch_username):
    users = load_users()
    
    # Trouver le prochain ID disponible
    user_id = str(len(users) + 1)
    
    # Hacher le mot de passe avant de le stocker
    hashed_password = generate_password_hash(password)

    # Ajouter l'utilisateur avec un identifiant unique
    users[user_id] = {
        "email": email,
        "password": hashed_password,
        "tiktok_username": tiktok_username,
        "twitch_username": twitch_username
    }
    
    # Sauvegarder les utilisateurs dans le fichier JSON
    save_users(users)

# @app.route('/home', methods=['GET', "POST"])
# def home():

#     username = None
#     min_views = None
#     max_view = None

#     if request.method  == 'POST':
#         client_id = os.getenv("CLIENT_ID")
#         client_secret = os.getenv("CLIENT_SECRET")

#         access_token = get_access_token(client_id, client_secret)
        
#         username = request.form.get('username')
#         min_views = request.form.get('min_views')
#         max_views = request.form.get('max_views')

#         client_id = os.getenv("CLIENT_ID")
#         client_secret = os.getenv("CLIENT_SECRET")

#         print (f"Informations sur les clips recuperees : Username : {username} ; minViews : {min_views} ; maxViews : {max_views}")
        
#         # Exemple d'utilisation 
#         channel_name = username  
#         clips = get_clips(channel_name, access_token, client_id)
#         print("Clips récupérés :", clips)

      
#         #faut voir avec wael parceque y'a une erreur avec la fonction access token.
#         #faut rajouter les param de views dans get_clips si on veux se param
      
#     return render_template('home.html', title="Home")

@app.route('/', methods=['GET', "POST"])
def home():
    videos_downloaded = []
    error = None
    
    
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    email = session['email']
    with open("Twitok_Bot\\src\\metadata\\users.json", 'r') as f:
        data = json.load(f)
        for e in data:
            print(data[e]["email"] , email)
            if data[e]["email"] == email:
                session["twitch_username"] = data[e]["twitch_username"]
    
    

    if request.method == 'POST':
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        try:
            # access_token = get_access_token(client_id, client_secret)

            username = request.form.get('username')
            min_views = request.form.get('min_views', type=int)
            max_views = request.form.get('max_views', type=int)

            # Récupère les clips
            # clips = get_clips(username, access_token, client_id)
            # print(f"Clips récupérés : {clips}")

            # Filtrer les clips par vues si min_views ou max_views sont fournis
            if min_views or max_views:
                clips = [
                    clip for clip in clips
                    if (min_views is None or clip['view_count'] >= min_views) and
                       (max_views is None or clip['view_count'] <= max_views)
                ]
           

            # Télécharger les clips
            for clip in clips:
                print("telechargement en cours ...")
                # download_clip_with_audio(clip)
                videos_downloaded.append(clip['title'])  # Stocke les titres pour affichage

        except Exception as e:
            error = str(e)  # En cas d'erreur, stockez le message

    return render_template('home.html', title="Home" ,username=session['twitch_username'], videos=videos_downloaded, error=error)

@app.route('/restart', methods=['POST'])
def restart_server():
    """Redémarrer le serveur."""
    if request.method == 'POST' or request.method == 'GET':
        # Arrêter le processus Flask actuel
        print("Arrêt du serveur Flask...")
        # Attendre un peu pour permettre au serveur de s'arrêter proprement
        time.sleep(1)
        # Redémarrer le serveur Flask
        print("Redémarrage du serveur Flask...")

    return "Redémarrage du serveur...", 200  # Retour à l'utilisateur

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Charger les utilisateurs depuis le fichier JSON
        users = load_users()

        # Rechercher l'utilisateur par email
        for user in users.values():
            if user["email"] == email:
                # Vérifier le mot de passe
                if check_password_hash(user["password"], password):
                    session['logged_in'] = True
                    session['email'] = email
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password.', 'error')
                    return redirect(url_for('login'))

        flash('email not found.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html', title="Home")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tiktok_username = request.form.get('tiktok_username')
        twitch_username = request.form.get('twitch_username')

        # Charger les utilisateurs depuis le fichier JSON
        users = load_users()

        # Vérifier si l'email existe déjà
        for user in users.values():
            if user["email"] == email:
                flash('Email already registered.', 'error')
                return render_template('signup.html', title="Signup")  # Recharger la page sans redirection

        # Ajouter l'utilisateur dans le fichier JSON avec un identifiant unique
        add_user(email, password, tiktok_username, twitch_username)

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', title="Signup")


@app.route('/download', methods=['POST'])
def download_video():
    # Récupération de l'ID du clip envoyé depuis le formulaire
    video_id = request.form.get('id')

    if not video_id:
        return "Erreur : Aucun ID de clip fourni.", 400  # Vérifie et renvoie une erreur explicite
    
    print(f"ID de clip reçu : {video_id}")

    # Utiliser la fonction `get_clips` pour récupérer le clip à partir de son ID (ajuste la fonction si nécessaire)
    try:
        # Vous devez adapter cette partie pour récupérer un clip en fonction de l'ID (exemple simplifié)
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        # access_token = get_access_token(client_id, client_secret)
        # clips = get_clips(None, access_token, client_id)  # Filtrer pour obtenir le clip avec l'ID spécifié
        
        # Recherche du clip correspondant à l'ID
        # clip = next((clip for clip in clips if clip['id'] == video_id), None)
        
        # if not clip:
        #     return f"Erreur : Le clip avec l'ID {video_id} n'a pas été trouvé.", 404
        
        # # Utiliser la fonction pour télécharger le clip avec audio
        # save_path = "clips"  # Chemin où les clips seront sauvegardés
        # download_clip_with_audio(clip, save_path)

        # Chemin du fichier téléchargé
        # file_name = f"{save_path}/{clip['id']}.mp4"

        # # Vérifier si le fichier a bien été téléchargé
        # if os.path.exists(file_name):
        #     return send_file(file_name, as_attachment=True, download_name=f"{clip['id']}.mp4")
        # else:
        #     return f"Erreur : Le fichier du clip {video_id} n'a pas pu être téléchargé.", 500
        

    except Exception as e:
        return f"Erreur lors du téléchargement du clip : {str(e)}", 500


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créez une instance de l'API TikTok
# tiktok_api = tiktok_api.TikTokAPI()

# Route pour afficher la page HTML d'upload sur TikTok
@app.route('/upload_to_tiktok', methods=['GET'])
def upload_to_tiktok_page():
    return render_template('upload_to_tiktok.html')

# Route pour télécharger la vidéo sur TikTok via un POST
@app.route('/upload_to_tiktok', methods=['POST'])
def upload_video_to_tiktok():
    # Vérification du fichier vidéo téléchargé
    if 'videoFile' not in request.files:
        return jsonify({'error': 'Aucun fichier vidéo trouvé.'}), 400
    
    video_file = request.files['videoFile']
    caption = request.form.get('caption', '')

    if video_file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné.'}), 400
    
    # Sauvegarder la vidéo téléchargée dans le répertoire de stockage
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)

    # Publier la vidéo sur TikTok (exemple d'appel API)
    try:
        files = {'videoFile': open(video_path, 'rb')}
        data = {'caption': caption}
        
        response = requests.post('http://localhost:5000/upload_to_tiktok', files=files, data=data)

        if response.status_code == 200:
            return jsonify({'message': 'Vidéo téléchargée avec succès sur TikTok!'}), 200
        else:
            return jsonify({'error': f"Erreur lors de l'upload sur TikTok : {response.text}"}), 500
    except Exception as e:
        return jsonify({'error': f"Erreur lors de l'envoi à TikTok : {e}"}), 500
None




if __name__ == '__main__':
    app.run(debug=True)
