# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('Data/songs_listened_to_with_all_info_unique.csv')
one_hot_df = pd.concat([df.drop('month', axis=1), pd.get_dummies(df['Season'])], axis=1)
one_hot_df.to_csv('output.csv')

df['Count'] = 1
count_df = df.groupby('trackName', as_index = False).sum('Count')
count_df[['trackName', 'Count']]


# Split the data into training and testing sets
features = one_hot_df[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 1, 2, 3, 4]]
features.columns = features.columns.astype(str)
labels = pd.merge(one_hot_df, count_df, on='trackName')['Count']
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#Fitting model with trainig data
# Import the model we are using

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(features, labels)

# Saving model to disk
pickle.dump(rf, open('model.pkl','wb'))

'''
# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[2, 9, 6]]))
'''