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
import requests
import numpy as np

spotify_lst = ['606FB2E4VYYs9CJSLCnhUa', '4Ur5dnjKkGgjPSJpwKBHDd', 
               '5zP5a7VWRgvjCi6ra3IeJ0', '7CIeE38SdXZ9J0M76QRhmS',
               '0H3MpEFBNTXwPzPqz8yj6V', '69dtPFfkYa5URry1zo665z',
               '5ows8MyC8CN95GTbgTovnd', '6q6DzFMMwpYeU2a90J5IyJ',
               '3DyizJDVdHipO17XqQeK5f', '4J4rsjuzvXNcF996nPP2pG',
               '7MMIVoteyDNzNp7PJUCeG4', '6BGXLlqwvOkM4JdWXxjmER',
               '6EaLmdD8KZvXiBER0VgY8L', '1bk6tO6d5oes6n0vhACi5x',
               '74BP9iaXq354DmPUepjzNC', '1ux0KmjmnQCNQzQ0BH7kbl',
               '3lluUY967E5z4WnNeJKDV2', '2FEAysct4thAiYGojrHKlM',
               '3fniVM8pbMq8jcR23aVIY8', '6D0WkFzwCx5pxfD5jX0wkL',
               '6taan6n01bwB2B7EtN9KYI', '2mI2QBJDL4klpigMkqaFs5',
               '61FusglQju0yXpz3v7nYd5', '0p6VwHqAZNV9xw5HuIKHJd',
               '35wZqszdyXNFCAztyLWlgT', '7A1EbS3Zux6zhXyeSpHEx9',
               '5zYgmmRp9ozLstVry1JLbw', '0YKbjLgCPsp7K3k2JH4NZw',
               '6NewzRggzRDBBPowRuXBor', '0ytSNwG5nGYtB01bnmy4CY',
               '7gTvhRcUZaXt8ydN3AAIqF', '6sBduygGNeCecOenI9ZZ2F',
               '0vqKnSeWspiQ9EHhWM8ZFD', '6B7HuyxqWvbBkFMErD64VC',
               '2nAvu6nKy5YMZnjJjAA5et', '1FtOhbe9MmxVq3yhU9AYzP',
               '71ok4KKSKzVKTudbTsyLFS', '2wkM6gBP77AQB4hFwutvy4',
               '5DxEF8AgbkfjixhPVzRTqA', '4Qk6DsuSEp34mm8K7MuXH9',
               '1uFaOr8h7OeCG1atiUGaVN', '7iUo5BVXvkRKzzlX0ozIdA',
               '6qsTClrBMf59rUNnD3fzWc', '2Inm8T8QcA90nbOGshxHLo',
               '6AihpQrTXtgDnkcQwLfxYb', '5ohzMZ3OBvDlHypXCBKrHa',
               '3XdhaqlOYFr5484hWYHmTB', '5cIzPoYKkD0HtGKZ0ZDWMx',
               '1WvCS1o0lfs66CSxo4Ex49', '4bSNhfnKA9mr3ARsMpnau0']

class go_spotify(object):
    """ Extract spotify song data using spotify web API.
        Requires client id and secret key during initialization.
    """
    def __init__(self, cid, secret):
        self.cid = cid
        self.secret = secret
        credentials = SpotifyClientCredentials(client_id= cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)
        
    
    def songs_of_year(self, query, limit=50, length=10000):
        """Extracts all songs released during a certain year. 
           Parameters:
           query: takes as an input year for which you want to extract songs from
           limit (default-50): sets how many songs can extracted with one API call
           length (default 10,000): set how many total songs needs to be extracted
           
           Returns a dataframe containing artist name, track name, popularity, track id and release date.
        """
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
    
        df_tracks = pd.DataFrame({'artist_name':artist_name,'release_date':release_date,
                                  'track_name':track_name,'track_id':track_id,'popularity':popularity})
        df_tracks.drop_duplicates(subset=['artist_name','track_name'], inplace=True)
        return df_tracks
    
    
    def get_features(self, df_tracks, track_id, to_csv=False, y=None):
        ''' extract audio features of songs from spotify web api
            Takes as input as dataframe series containing song track id and it extracts 14 audio features from spotify
            Returns the dataframe with audio features merged into the queried dataframe.
            
            
            Parameters:
            df_tracks : dataframe containing song details
            track_id : dataframe series containing track id of songs, assumes it is the same length as df_tracks
            to_csv (default False): write the dataframe into a CSV file
            
        '''
        data = []
        limit = 100 
        noval = 0

        for i in range(0,len(track_id), limit):
            batch = track_id[i:i+limit]
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
        """ Takes as input a list containing all the years for which audio features of songs are required
            Returns an output containing a dataframe with songs for each year.
        """
        frames = []
        for year in year_list:
            tracks = self.songs_of_year(year)
            frame = self.get_features(tracks, tracks['track_id'], y=year)
            frames.append(frame)
        df = pd.concat(frames)
        if to_csv:
            df.to_csv(r'Song Dataset.csv')
        else:
            return df


def get_auth():
    CLIENT_ID ='50b2240e93784d028ba2eb626095dd6c'
    CLIENT_SECRET = '07e055a4f4fe4b9d83ad3e6961bb40f2'

    credentials = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    token = credentials.get_access_token()
    return "Bearer " + token


def get_tracks(lst = spotify_lst, oath =None):
    x= 1969
    df_list=[]
    for playlist in lst:
    

        r = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist}/tracks",
        headers={ "Accept": "application/json", "Content-Type": "application/json", "Authorization": oath})
        dat =r.json()
        
        data = dat['items']
        tracks_list=[]

        for i in range(0,len(data)):
           
            tracks_list.append({"track_name" : data[i]['track']['name'], "artist" : data[i]['track']['artists'][0]['name'],
                "album" : data[i]['track']['album']['name'], "release_date" : data[i]['track']['album']['release_date'],  
                "year" : x, "explicit" : data[i]['track']['explicit'], 
                "artist_id" : data[i]['track']['artists'][0]['id'], "album_id" : data[i]['track']['album']['id'], 
                "track_id" : data[i]['track']['id']})
        
        df_list.append(pd.DataFrame(tracks_list))
        
        x += 1
        
    tracks_df = pd.concat(df_list)
    tracks_df = tracks_df.reset_index()
    tracks_df.drop('index', axis = 1, inplace=True)
    return tracks_df

def get_missing_tracks(df, oath=None):
    null_df =df[df.track_id.isnull()]
    null_track_info = []
    count = 0
    for row in null_df.itertuples():
        track = getattr(row, 'track_name').replace(" ", "%20")
        artist = getattr(row, 'artist').replace(" ", "%20")
        
        
        q = requests.get(
            f"https://api.spotify.com/v1/search?q=track:{track}%20artist:{artist}&type=track" ,
            headers={ "Accept": "application/json", "Content-Type": "application/json", "Authorization": oath},
            params= {'limit':1})
        try:
            null_track = q.json()
            
            null_track_info.append({'release_date': null_track['tracks']['items'][0]['album']['release_date'], 
                'explicit': null_track['tracks']['items'][0]['explicit'],
                'artist_id': null_track['tracks']['items'][0]['artists'][0]['id'],
                'album_id': null_track['tracks']['items'][0]['album']['id'],
                'track_id': null_track['tracks']['items'][0]['id']})
        except(IndexError):
             null_track_info.append({'release_date': np.nan, 
                'explicit': np.nan,
                'artist_id': np.nan ,
                'album_id': np.nan,
                'track_id': np.nan })
             
        count +=1
    null_track_info_df = pd.DataFrame(null_track_info, index=null_df.index)
    null_df.fillna(null_track_info_df, inplace=True)
    df.fillna(null_df, inplace = True)
    df.dropna(inplace = True)
    return df

def get_track_info(df, oath = None):
    track_info=[]
    for row in df.itertuples():
        track_id = getattr(row, 'track_id')
        
        q = requests.get(
            f"https://api.spotify.com/v1/audio-features/{track_id}" ,
            headers={ "Accept": "application/json", "Content-Type": "application/json", "Authorization": oath})
        track_features = q.json()
        try:
            track_info.append({'danceability': track_features['danceability'], 'energy': track_features['energy'],
                           'key': track_features['key'], 'loudness': track_features['loudness'], 
                           'mode': track_features['mode'], 'speechiness': track_features['speechiness'],
                           'acousticness': track_features['acousticness'], 
                           'instrumentalness': track_features['instrumentalness'], 'liveness': track_features['liveness'],
                           'valence': track_features['valence'], 'tempo': track_features['tempo'], 
                           'duration_ms': track_features['duration_ms'], 'time_signature': track_features['time_signature']})
        except(KeyError):
            track_info.append({'danceability': np.nan, 'energy': np.nan, 'key': np.nan, 'loudness': np.nan, 'mode': np.nan, 
                               'speechiness': np.nan, 'acousticness': np.nan, 'instrumentalness': np.nan, 'liveness': np.nan,
                               'valence': np.nan, 'tempo': np.nan, 'duration_ms': np.nan, 'time_signature': np.nan})
    
    track_info_df = pd.DataFrame(track_info)
    df= df.join(track_info_df)

    return df

def get_data(lst=spotify_lst):
    oath = get_auth()
    tracks_df = get_tracks(oath =oath)
    tracks_df = get_missing_tracks(df = tracks_df,oath =oath)
    return  get_track_info(df = tracks_df, oath =oath)
def seasons(m):
    if (m >= 3 and m <=5):
        return 'spring'
    elif (m >= 6 and m <=8):
        return 'summer'
    elif (m >= 9 and m <=11):
        return 'fall'
    else:
        return 'winter'


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
