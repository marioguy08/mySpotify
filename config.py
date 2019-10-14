# SRC: https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Recaptcha Keys
RECAPTCHA_PUBLIC_KEY    = ''
RECAPTCHA_PRIVATE_KEY   = ''

SPOTIFY_CLIENT_ID       = ''
SPOTIFY_CLIENT_SECRET   = ''
SPOTIFY_API_BASE_URL    = 'https://api.spotify.com/v1'
SPOTIFY_AUTH_URL        = 'https://accounts.spotify.com'
SPOTIFY_REDIRECT_URI    = 'http://192.168.88.249:8080/auth/callback'
SPOTIFY_SCOPE           = 'playlist-read-private user-follow-read user-read-private'

login_manager_secret_key= b'\xdc\x95!B1\xa0\xea:\xea\x8dn\'\xef~;I\x86Z\x9aSY\xde\x9cY\xbc_\x9e\xaf\x05&"\x07'