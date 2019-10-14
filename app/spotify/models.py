import requests
import config
import base64

class Spotify():
    def __init__(self, callback=None):
        self.callback = callback
        
        auth_str        = '{}:{}'.format(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET)
        b64_auth_str    = base64.urlsafe_b64encode(auth_str.encode()).decode()
        self.headers    = { 'Authorization': 'Basic {}'.format(b64_auth_str) }
    
    def update_callback(self, callback):
        return callback

    def current_user(self):
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/me', 'foo')
    
    def __get__(self, url, params=None):
        return requests.get(url=url, params=params)
    
    def __post__(self, url, headers=None, data=None):
        return requests.post(url, headers=self.headers, data=data)

    def get_tokens(self):
        data = {
            'grant_type'    : 'authorization_code',
            'code'          : self.callback,
            'redirect_uri'  : config.SPOTIFY_REDIRECT_URI
        }
        
        response = self.__post__(config.SPOTIFY_AUTH_URL + '/api/token', headers=self.headers, data=data).json()

        return response['access_token'], response['refresh_token']

    def refresh_auth_token(self, refresh_token):
        data = {
            'grant_type'    : 'refresh_token',
            'refresh_token' : refresh_token
        }

        response = self.__post__(config.SPOTIFY_AUTH_URL + '/api/token', headers=self.headers, data=data).json()

        return response['access_token']