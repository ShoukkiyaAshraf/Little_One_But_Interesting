import configparser
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def auth():
    config = configparser.ConfigParser()
    config.read('config_spotify.ini')
    id = config['Client_ID']['id']
    secret = config['Client_Secret']['secret']
    token = SpotifyClientCredentials(client_id=id, client_secret=secret).get_access_token(as_dict=False)
    return token


def getCategories():
    api_url = 'https://api.spotify.com/v1/browse/categories'
    token = auth()
    sp = spotipy.Spotify(token)
    headers = {"authorization": 'Bearer ' + token}
    params = {
        "country": "SE"
    }
    r = requests.get(api_url, headers=headers, params=params)
    categories = r.json()['categories']['items']
    id = []
    name = []
    for category in categories:
        id.append(category["id"])
        name.append(category["name"])
    return id, name, sp


def getCategoryPlaylist():
    category_id, category_name, sp = getCategories()
    for category in category_id:
        print(category, end='   ')
    category_id_selected = input("\n Select your category : ")
    limit = input("Enter the no. of playlist you need : ")
    playlists = sp.category_playlists(category_id_selected, limit=limit)
    playlist_id = []
    for playlist in playlists['playlists']['items']:
        try:
            playlist_id.append(playlist['id'])
        except:
            print('Cannot load ')
    return playlist_id, sp


def getPlaylistTrack():
    id_list, sp = getCategoryPlaylist()
    token = auth()
    end_point = "https://api.spotify.com/v1/playlists/{}/tracks"
    headers = {"authorization": "Bearer "+token}
    params = {
        "market": "ES"
    }
    track_id = []
    for id in id_list:
        r = requests.get(end_point.format(id), headers=headers, params=params)
        track_id.append(r.json()["items"][0]["track"]["id"])
    

print(getPlaylistTrack())
