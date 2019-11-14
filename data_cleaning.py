"""
This module is for your data cleaning.
It should be repeatable.

## PRECLEANING
There should be a separate script recording how you transformed the json api calls into a dataframe and csv.

## SUPPORT FUNCTIONS
There can be an unlimited amount of support functions.
Each support function should have an informative name and return the partially cleaned bit of the dataset.
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class go_spotify(object):
    """ Extract spotify song data using spotify web API.
    """
    def __init__(self, cid, secret):
        self.cid = cid
        self.secret = secret
        credentials = SpotifyClientCredentials(client_id= cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)
        
    
    def songs_of_year(self, query, limit=50, length=10000):
        artist_name = []
        track_name = []
        popularity = []
        track_id = []
        release_date = []
        
        for i in range(0,10000,50):
            track_results = self.sp.search(q='year:{}'.format(query), type='track', limit=50, offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                try:
                    release_date.append(t['album']['release_date'])
                except:
                    release_date.append('?')
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])
    
        df_tracks = pd.DataFrame({'artist_name':artist_name,'release_date':release_date,'track_name':track_name,'track_id':track_id,'popularity':popularity})
        df_tracks.drop_duplicates(subset=['artist_name','track_name'], inplace=True)
        return df_tracks
    
    
    def get_features(self, df_tracks, to_csv=False, y=None):
        data = []
        limit = 100 
        noval = 0

        for i in range(0,len(df_tracks['track_id']), limit):
            batch = df_tracks['track_id'][i:i+limit]
            feature_results = self.sp.audio_features(batch)
            for i, t in enumerate(feature_results):
                if t == None:
                    noval += 1
                else:
                    data.append(t)

        print('Number of tracks where no audio features were available for year {}:'.format(y),noval)
        print('number of songs:', len(data))
        df_audio_features = pd.DataFrame.from_dict(data,orient='columns')
        columns_to_drop = ['analysis_url','track_href','type','uri']
        df_audio_features.drop(columns_to_drop, axis=1,inplace=True)
        df_audio_features.rename(columns={'id': 'track_id'}, inplace=True)
        df = pd.merge(df_tracks,df_audio_features,on='track_id',how='inner')
        if to_csv:
            df.to_csv(r'song features.csv')
        else:
            return df
        
    
    
    def get_many_years(self, year_list, to_csv=False):
        frames = []
        for year in year_list:
            frame = self.get_features(self.songs_of_year(year), y=year)
            frames.append(frame)
        df = pd.concat(frames)
        if to_csv:
            df.to_csv(r'Song Dataset.csv')
        else:
            return df



def support_function_one(example):
    pass

def support_function_two(example):
    pass

def support_function_three(example):
    pass

def full_clean():
    """
    This is the one function called that will run all the support functions.
    Assumption: Your data will be saved in a data folder and named "dirty_data.csv"

    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    dirty_data = pd.read_csv("./data/dirty_data.csv")

    cleaning_data1 = support_function_one(dirty_data)
    cleaning_data2 = support_function_two(cleaning_data1)
    cleaned_data= support_function_three(cleaning_data2)
    cleaned_data.to_csv('./data/cleaned_for_testing.csv')
    
    return cleaned_data