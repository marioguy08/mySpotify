import requests
import config
import base64

class Spotify():
    def __init__(self, callback=None):
        self.callback = callback
        
        auth_str            = '{}:{}'.format(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET)
        b64_auth_str        = base64.urlsafe_b64encode(auth_str.encode()).decode()
        self.auth_headers   = self.get_headers('Basic', b64_auth_str)
    
    def update_callback(self, callback):
        return callback

    def __get__(self, url, params=None, headers=None):
        return requests.get(url=url, params=params, headers=headers)
    
    def __post__(self, url, headers=None, data=None):
        return requests.post(url, headers=self.auth_headers, data=data)

    def __spotify_get_items__(self, url, access_token, limit):
        headers = self.get_headers('Bearer', access_token)
        params  = {'limit': limit}

        response = self.__get__(url, params=params, headers=headers).json()
        items = response['items']

        while response['next'] is not None:
            response = self.__get__(response['next'], params=params, headers=headers).json()
            items.extend(response['items'])

        return items

    def get_headers(self, type, access_token):
        return {'Authorization': '{} {}'.format(type, access_token)}

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
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/me', headers=self.get_headers('Bearer', access_token)).json()['display_name']
    
    def get_spotify_user_id(self, access_token):
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/me', headers=self.get_headers('Bearer', access_token)).json()['id']
    
    def get_spotify_profile_picture_url(self, access_token):
        response = self.__get__(config.SPOTIFY_API_BASE_URL + '/me', headers=self.get_headers('Bearer', access_token)).json()
        if response['images'] == []:
            return 'https://static.change.org/profile-img/default-user-profile.svg'
        return response['images'][0]['url']

    def get_spotify_current_user_playlists(self, access_token):
        return self.__spotify_get_items__(config.SPOTIFY_API_BASE_URL + '/me/playlists', access_token, 50)

    def get_spotify_user_playlists(self, access_token, id):
        return self.__spotify_get_items__(config.SPOTIFY_API_BASE_URL + '/users/{}/playlists'.format(id), access_token, 50)

    def get_spotify_song_feature(self, access_token, id):
        return self.__get__(config.SPOTIFY_API_BASE_URL + '/audio-features/' + id, headers=self.get_headers('Bearer', access_token)).json()

    def get_spotify_songs_feature(self, access_token, ids):
        return self.__get__('{}/audio-features/?ids={}'.format(config.SPOTIFY_API_BASE_URL, ','.join(ids)), headers=self.get_headers('Bearer', access_token)).json()['audio_features']

    def get_spotify_playlist_tracks(self, access_token, id):
        return self.__spotify_get_items__(config.SPOTIFY_API_BASE_URL + '/playlists/{}/tracks'.format(id), access_token, 100)