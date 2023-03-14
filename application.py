import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from cleaning import convert_playlist_to_uris, get_playlist_stats_from_uris
from datetime import datetime
import json
# import warnings
# warnings.filterwarnings("ignore")

application = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb'))

@application.route('/')
def home():
    return render_template('index.html')

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
    f = open('key.json')
    keys = json.load(f)
    if keys['cid'] and keys['secret']:
        application.run(debug=True)
    else:
        print("Need to get your CID and Secret from Spotify API first! https://developer.spotify.com/dashboard/")
