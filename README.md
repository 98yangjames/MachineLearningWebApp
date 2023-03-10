## Deploying ML Model using Flask
This is a simple project to elaborate how to deploy a Machine Learning model using Flask API

### Prerequisites
You must have Scikit Learn, Pandas (for Machine Leraning Model) and Flask (for API) installed.

Flask version: 0.12.2
conda install flask=0.12.2  (or) pip install Flask==0.12.2

### Project Structure
This project has four major parts :
1. model.py - This contains code for our Machine Learning Random Forest model that predicts the number of times I would listen to a song.
2. application.py - This contains Flask APIs that receives employee details through GUI or API calls, computes the precited value based on our model and returns it.
3. template - This folder contains the HTML template (index.html) to allow user to enter Spotify Playlist Link to output the song plays on each of the songs (rounded, so it won't show all songs if it is less than 1).
4. static - This folder contains the css folder with style.css file which has the styling required for out index.html file.

### Running the project
1. Ensure that you are in the project home directory. Create the machine learning model by running below command from command prompt -
```
python model.py
```
This would create a serialized version of our model into a file model.pkl

2. Run app.py using below command to start Flask API
```
python app.py
```
If you are getting the message "Need to get your CID and Secret from Spotify API first! https://developer.spotify.com/dashboard/", please go to the dashboard and get your unique CID and secret values. In lines 10 and 11 on application.py

By default, flask will run on port 5000.

3. Navigate to URL http://127.0.0.1:5000/ (or) http://localhost:5000

You should be able to view the homepage.

![image](https://user-images.githubusercontent.com/45018941/224507826-7371dc1e-5693-4362-bfe6-1c4c254128b8.png)

