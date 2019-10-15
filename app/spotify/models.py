import requests
import config
import base64

class Spotify():
    def __init__(self, callback=None):
        self.callback = callback
        
        auth_str        = '{}:{}'.format(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET)
        b64_auth_str    = base64.urlsafe_b64encode(auth_str.encode()).decode()
        self.auth_headers    = { 'Authorization': 'Basic {}'.format(b64_auth_str) }
    
    def update_callback(self, callback):
        return callback

    def __get__(self, url, params=None, headers=None):
        return requests.get(url=url, params=params, headers=headers)
    
    def __post__(self, url, headers=None, data=None):
        return requests.post(url, headers=self.auth_headers, data=data)

    def get_tokens(self):
        data = {
            'grant_type'    : 'authorization_code',
            'code'          : self.callback,
            'redirect_uri'  : config.SPOTIFY_REDIRECT_URI
        }
        
        response = self.__post__(config.SPOTIFY_AUTH_URL + '/api/token', headers=self.auth_headers, data=data).json()

        return response['access_token'], response['refresh_token']

    def refresh_access_token(self, refresh_token):
        data = {
            'grant_type'    : 'refresh_token',
            'refresh_token' : refresh_token
        }

        return self.__post__(config.SPOTIFY_AUTH_URL + '/api/token', headers=self.auth_headers, data=data).json()['access_token']
    
    def get_spotify_username(self, access_token):
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/me', headers={'Authorization': 'Bearer {}'.format(access_token)}).json()['display_name']
    
    def get_spotify_profile_picture_url(self, access_token):
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/me', headers={'Authorization': 'Bearer {}'.format(access_token)}).json()['images'][0]['url']

    def get_spotify_user_playlists(self, access_token):
        url = config.SPOTIFY_API_BASE_URL + '/me/playlists'
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        params  = {'limit': 50}
        response = self.__get__(url, params=params, headers=headers).json()
        playlists = response['items']

        while response['next'] is not None:
            response = self.__get__(response['next'], params=params, headers=headers).json()
            playlists.extend(response['items'])
        
        return playlists
