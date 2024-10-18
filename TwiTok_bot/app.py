from flask import Flask, redirect, request, make_response
import requests
import random
import string

app = Flask(__name__)  # Initialize the Flask app

# Client credentials (replace with your actual credentials)
CLIENT_KEY = 'awora45879uzvqvt'  
CLIENT_SECRET = 'axvMcj73XxtKUTGWduuFE85F2giuadt2'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # Registered Redirect URI

def generate_random_string(length=64):
    """Generate a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')  # Home route
def home():
    return "TwikTok Bot"

@app.route('/oauth')  # OAuth route
def oauth():
    csrf_state = generate_random_string(16)
    response = make_response(redirect(
        f'https://www.tiktok.com/v2/auth/authorize/?client_key={CLIENT_KEY}&response_type=code&scope=user.info.basic&redirect_uri={REDIRECT_URI}&state={csrf_state}&code_challenge={csrf_state}&code_challenge_method=S256'
    ))
    response.set_cookie('csrfState', csrf_state, max_age=600)  # Store CSRF state in a cookie
    return response

@app.route('/callback')  # Callback route
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if error:
        return f"Error: {request.args.get('error_description')}", 400

    # Check the CSRF state
    if state != request.cookies.get('csrfState'):
        return "Invalid state parameter", 403

    # Exchange the authorization code for an access token
    access_token = get_access_token(code)
    return f"Access Token: {access_token}"

def get_access_token(code):
    """Exchange the authorization code for an access token."""
    token_url = 'https://open-api.tiktok.com/oauth/access_token/'
    payload = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=payload)
    data = response.json()
    
    if data.get('code') == 0:
        return data['data']['access_token']
    else:
        return f"Error getting access token: {data}"

if __name__ == '__main__':
    app.run(port=5000)
