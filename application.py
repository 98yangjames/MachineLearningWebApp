import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from datetime import datetime
cid = '7cda6c1856a24d109ba5521fd35fd5a3'
secret = 'ac6d7cd270aa48cab17e179262d78031'
application = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb'))

@application.route('/')
def home():
    return render_template('index.html')

def convert_playlist_to_uris(playlist_link):

        
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
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
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
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
    
@application.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    form_inputs = [str(x) for x in request.form.values()]
    convert_playlist_to_uris(form_inputs[0])
    stats = get_playlist_stats_from_uris()
    final_features = stats
    predictions = model.predict(final_features.drop('trackName', axis=1))

    output = predictions.round(2)
    prediction_df = pd.DataFrame()
    prediction_df['Count'] = predictions.round(2)
    prediction_df['trackName'] = list(stats['trackName'])
    # prediction_df['trackName'] = stats['trackName']
    prediction_df = prediction_df.sort_values('Count', ascending=False)
    prediction_df.rename(columns = {'trackName':'Track Name'}, inplace=True)
    #prediction_text='Song Names should be $ {}'.format(stats['trackName'])
    return render_template('index.html', row_data=list(prediction_df.values.tolist()), column_names=prediction_df.columns.values, tables=[prediction_df.to_html(classes='data')], titles=prediction_df.columns.values, zip=zip)

if __name__ == "__main__":
    application.run(debug=True)
