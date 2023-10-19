"""
Dataframe (Music Exploration Tool)
Author: Yvonne Teo
Description: This script deals with imported data.
"""

# IMPORTS
import streamlit as st

from methods import save_df, track_moods

# Page and app config
st.set_page_config(page_title="Music Exploration Tool - Data", page_icon="🎵",  layout="wide")
st.title("Spotify Data")

# Get data
df = st.session_state.df

# Show data in table form
st.markdown("#### The Data")
st.write(f"Dataframe dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
st.write("*You can edit fields in this dataframe, so play around with it, but be careful!*")
edited_df = st.experimental_data_editor(df)
st.write("")
reload_button = st.button("Reload data")
if reload_button:
    df = st.session_state.df
    st.success("Reloaded!")
save_button = st.button("Save data")
if save_button:
    fp = save_df(st.session_state.df)
    st.success("File has been successfully saved!")
add_cluster_button = st.button("Add clusters")
if add_cluster_button:
    if "cluster_labels" not in st.session_state:
        st.error("*You need to run clustering first!*")
    else:
        df["cluster"] = st.session_state.cluster_labels
        st.success("Added! Click the Add clusters button again or the Reload data button to see the updated dataframe.")

# Add notes and/or moods to dataframe
st.markdown("#### Add moods to dataframe")
with st.form("Add moods"):
    st.write("*You can also add these directly in through the dataframe above, but this helps with choosing moods!*")
    selected_row = st.selectbox(label="Select a track:",
                                options=df["name"])
    user_moods = st.multiselect("Choose moods:",
                                options=track_moods)
    user_notes = st.text_input("Enter your notes:")
    submitted_new_df = st.form_submit_button("Add mood and/or notes!")
    if submitted_new_df:
        df.loc[df["name"] == selected_row, "moods"] = ", ".join(user_moods)
        df.loc[df["name"] == selected_row, "notes"] = user_notes
        st.success("Added successfully!")
