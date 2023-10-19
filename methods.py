"""
Methods (Music Exploration Tool)
Author: Yvonne Teo
Description: This script includes methods used in the music exploration tool.
"""

# IMPORTS
import pickle
import spotipy
import time

import pandas as pd
import streamlit as st

from flatten_json import flatten
from os.path import exists
from spotipy.oauth2 import SpotifyClientCredentials

# DEFINITIONS
# Define features that are relevant
df_columns = [
    "name",
    "id",
    "artist",
    "tempo",
    "time_signature",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "track_num_samples",
    "track_duration",
    "track_end_of_fade_in",
    "track_start_of_fade_out",
    "track_tempo_confidence",
    "track_time_signature_confidence",
    "track_key_confidence",
    "track_mode_confidence",
    "duration_ms",
    "track_href",
    "analysis_url"
]

track_moods = [
    "anxious",
    "bittersweet",
    "boisterous",
    "bright",
    "cheerful",
    "chill",
    "dangerous",
    "dark",
    "elegant",
    "epic",
    "furious",
    "heavy",
    "hopeful",
    "intense",
    "laidback",
    "melancholy",
    "relaxed",
    "romantic",
    "sad/sorrowful",
    "sombre",
    "suspenseful",
    "tense",
    "warm",
    "wistful"
]

visual_cols = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "track_tempo_confidence",
    "track_time_signature_confidence",
    "track_key_confidence",
    "track_mode_confidence",
]

feature_cols = [
    "tempo",
    "time_signature",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "loudness",
    "valence",
    "track_num_samples",
    "track_duration",
    "track_tempo_confidence",
    "track_time_signature_confidence",
    "track_key_confidence",
    "track_mode_confidence",
    "duration_ms",
]


# HELPER METHODS
# GETTING DATA
@st.cache_data
def save_df(dataframe: pd.DataFrame) -> str:
    """Save a dataframe so that it doesn't need to be imported over and over again."""
    now = time.time()
    with open(f"./pickles/spotify_df{now}.pkl", "wb") as f:
        pickle.dump(dataframe, f)
    file_path = f"./pickles/spotify_df{now}.pkl"
    return file_path


@st.cache_data
def load_df(file_path: str) -> pd.DataFrame:
    """Load a dataframe - default is the dataframe saved.
    This can be changed to the master dataframe or another filepath."""
    dataframe = pd.read_pickle(file_path)
    return dataframe


@st.cache_data
def save_master_df(dataframe: pd.DataFrame):
    """Save a master dataframe."""
    path = "./pickles/spotify_master_df.pkl"
    if exists(path):
        df_master = pd.read_pickle(path)
        df_master = pd.concat([df_master, dataframe])
        df_master = df_master.drop_duplicates()
        with open(path, "wb") as f:
            pickle.dump(df_master, f)
    else:
        with open(path, "wb") as f:
            pickle.dump(dataframe, f)


# Spotipy (Spotify API) Configuration
@st.cache_resource
def get_spotipy_info(user_cid, user_secret):
    """Get information for Spotipy (Spotify API for Python)."""
    cid = user_cid
    secret = user_secret
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret)
    my_spotipy = spotipy.Spotify(client_credentials_manager=client_credentials_manager,
                                 requests_timeout=10,
                                 retries=10)
    return my_spotipy


# Get Spotify playlist data
@st.cache_data
def get_playlist(_sp, playlist_id) -> dict:
    """Get the playlist items as a nested dictionary."""
    playlist_items = _sp.playlist_items(playlist_id=playlist_id)
    return playlist_items


# Get Spotify playlist dataframe
@st.cache_data
def get_artists(track_artist: list) -> str:
    """Get artists as a string from nested structure."""
    track_artists = []
    for artist_list in track_artist:
        track_artists.append(artist_list["name"])
    artist = ", ".join(track_artists)
    return artist


# Get audio features from track id through Spotify API
@st.cache_data
def get_audio_features(_sp, track_id) -> pd.DataFrame:
    """Get audio features of the track from Spotify API."""
    features = _sp.audio_features(tracks=[track_id])
    df_features = pd.DataFrame(features)
    return df_features


# Get audio features from track id through Spotify API
@st.cache_data
def get_audio_analysis(_sp, track_id) -> pd.DataFrame:
    """Get audio analysis of the track from Spotify API."""
    analysis = _sp.audio_analysis(track_id=track_id)
    remove_keys = ["bars", "beats", "segments", "tatums", "meta"]
    for key in remove_keys:
        analysis.pop(key, None)
    analysis_dict = flatten(analysis)
    df_analysis = pd.DataFrame.from_dict(analysis_dict, orient="index")
    df_analysis = df_analysis.transpose()
    return df_analysis


# Create a dataframe from Spotify playlist
@st.cache_data
def create_df(_sp, sp_playlist) -> pd.DataFrame:
    """Create a dataframe from the Spotify playlist."""
    dataframe = pd.DataFrame()
    for item in sp_playlist["items"]:
        track_id = item["track"]["id"]
        df_features = get_audio_features(_sp, track_id)
        df_analysis = get_audio_analysis(_sp, track_id)
        df_full = pd.concat([df_features, df_analysis], axis=1)
        track_artist = item["track"]["artists"]
        df_full["artist"] = get_artists(track_artist)
        df_full["name"] = item["track"]["name"]
        dataframe = pd.concat([dataframe, df_full], ignore_index=True)
    return dataframe


# Clean dataframe to only take the columns we want
@st.cache_data
def clean_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe to only take relevant columns and add relevant columns."""
    dataframe = dataframe[df_columns]
    new_columns = ["moods", "notes", "cluster"]
    for col in new_columns:
        if col not in dataframe.columns:
            dataframe[col] = ""
    return dataframe
