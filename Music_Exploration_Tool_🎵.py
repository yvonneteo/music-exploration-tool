"""
Music Exploration Tool
Author: Yvonne Teo
Description: This tool is a prototype for musicians, specifically media composers, to explore different music trends
in a visual way on a larger scale than typical music analysis.
"""

# IMPORTS
import streamlit as st

from methods import create_df, clean_df, get_playlist, get_spotipy_info, load_df, save_df, save_master_df


# Page and app config
st.set_page_config(page_title="Music Exploration Tool", page_icon="🎵", layout="wide")
st.title("Music Exploration Tool")
st.set_option("deprecation.showPyplotGlobalUse", False)

st.subheader("Import data")
# GETTING DATA
with st.form("import_data"):
    st.markdown("**Import data here:** 👇")
    import_existing = st.radio(label="Import existing dataframe?",
                               options=["Yes, import pickled dataframe",
                                        "No, fetch new data from Spotify API"])
    st.write("")
    st.write("Existing dataframe import settings:")
    open_path = st.text_input(label="File path for dataframe",
                              value="./pickles/spotify_master_df.pkl")
    st.write(""
             "")
    st.write("Spotify API settings:")
    st.write("Follow the following steps if you don't have a Spotify developer account yet.")
    st.write("Step 1: Log in to Spotify Developer or create a free Spotify Developer account.")
    st.write(
        "Step 2: In your dashboard, click the green 'Create a Client ID' button and fill in the form to create an app.")
    st.write("Step 3: Click on the new app you just created to find your Client ID (Spotify CID) and User Secret.")
    user_cid = st.text_input(label="Spotify CID",
                             value="",
                             placeholder="Please paste your Spotify CID here")
    user_secret = st.text_input(label="Spotify User Secret",
                                value="",
                                placeholder="Please paste your Spotify User Secret here")
    playlist_id = st.text_input(label="Playlist ID or URL",
                                placeholder="e.g. 3j1iDQdjbP8tUcNbe4BVhz")
    submitted_import = st.form_submit_button("Import data")
    if submitted_import:
        if import_existing == "No, fetch new data from Spotify API":
            sp = get_spotipy_info(user_cid, user_secret)
            playlist_df = create_df(sp, get_playlist(sp, playlist_id))
            df_clean = clean_df(playlist_df)
            fp = save_df(df_clean)
        else:
            fp = open_path
            df_clean = load_df(fp)
        save_master_df(df_clean)
        st.session_state.df = df_clean
        if "df" in st.session_state:
            st.success("Data imported successfully!")
        else:
            st.error("Something must have gone wrong. Please check the fields again.")
