import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
from werkzeug.security import generate_password_hash, check_password_hash
from Api.Tiktok.tiktok import login



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez par une clé secrète

# Le chemin vers le fichier JSON pour stocker les utilisateurs
USER_DATA_FILE = 'users.json'

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

@app.route('/home', methods=['GET', "POST"])
def home():

    username = None
    min_views = None
    max_view = None

    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

    if request.method  == 'POST':
        username = request.form.get('username')
        min_views = request.form.get('min_views')
        max_views = request.form.get('max_views')

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

      
        #faut voir avec wael parceque y'a une erreur avec la fonction access token.
        #faut rajouter les param de views dans get_clips si on veux se param
      
    return render_template('home.html', title="Home")


@app.route('/tiktok', methods=['GET', "POST"])
def tiktok():
    username = None
    password = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # utiliser la fonction login de tiktok avec comme param username et password du form
        

    return render_template('tiktok.html', title="Tiktok")

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
                    session["logged_in"] = True
                    session["email"] = email
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password.', 'error')
                    return redirect(url_for('login'))

        flash('Email not found.', 'error')
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





if __name__ == '__main__':
    app.run(debug=True)
