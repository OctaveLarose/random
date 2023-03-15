## This code was mostly written by ChatGPT, which got it shockingly right on its first attempt. Rest was myself.

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from functools import reduce

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id, additional_types=('track',))
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = os.environ.get('PLAYLIST_ID')
playlist = sp.playlist(playlist_id)

all_tracks = get_playlist_tracks(playlist_id)
artists = [[artist["name"] for artist in track['track']['artists']] for track in all_tracks]
flattened_artists_list = reduce(lambda xs, ys: xs + ys, artists)

duplicates = [x for x in flattened_artists_list if flattened_artists_list.count(x) > 1]
print(duplicates)