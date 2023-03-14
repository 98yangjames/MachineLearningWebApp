from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
from datetime import datetime
import json

f = open('key.json')
keys = json.load(f)

def convert_playlist_to_uris(playlist_link):

    client_credentials_manager = SpotifyClientCredentials(client_id=keys['cid'], client_secret=keys['secret'])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlist_dict = sp.playlist(playlist_link)
    # Get playlist Uris
    playlist_uris = []
    trackNames = []
    df = pd.DataFrame()
    for i in range(len(playlist_dict)):
        playlist_uris.append(playlist_dict['tracks']['items'][i]['track']['uri'])
        trackNames.append(playlist_dict['tracks']['items'][i]['track']['name'])

    df['trackName'] = trackNames
    df['uri'] = playlist_uris
    df.to_csv('Data/playlist.csv')

def get_playlist_stats_from_uris():
    df = pd.read_csv('Data/playlist.csv')
    client_credentials_manager = SpotifyClientCredentials(client_id=keys['cid'], client_secret=keys['secret'])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)   
    stats = pd.DataFrame()
    for i in df['uri']:    
        song_stats = pd.DataFrame.from_dict(sp.audio_features(i)).drop(['type', 'mode', 'id', 'uri', 'track_href', 'analysis_url', 'time_signature', 'duration_ms'], axis = 1)
        stats = stats.append(song_stats)
    
    currentMonth = datetime.now().month
    season = 0
    if currentMonth in [12,1,2]:
        season = 1
        stats['1'] = 1
        stats['2'] = 0
        stats['3'] = 0
        stats['4'] = 0
    elif currentMonth in [3,4,5]:
        season = 2
        stats['1'] = 0
        stats['2'] = 1
        stats['3'] = 0
        stats['4'] = 0
    elif currentMonth in [6,7,8]:
        season = 3
        stats['1'] = 0
        stats['2'] = 0
        stats['3'] = 1
        stats['4'] = 0
    elif currentMonth in [9,10,11]:
        season = 4
        stats['1'] = 0
        stats['2'] = 0
        stats['3'] = 0
        stats['4'] = 1
    stats['trackName'] = list(df['trackName'])
    stats.to_csv('Data/playlist_stats.csv')
    return stats


