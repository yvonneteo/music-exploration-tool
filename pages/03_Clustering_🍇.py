"""
Clustering (Music Exploration Tool)
Author: Yvonne Teo
Description: This script deals with the clustering of the data.
"""

# IMPORTS
import pandas as pd
import plotly.colors as pc
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import minmax_scale
from methods import feature_cols, visual_cols


# Page and app config
st.set_page_config(page_title="Music Exploration Tool - Unsupervised Clustering", page_icon="🎵",  layout="wide")
st.title("Clustering of Spotify Playlist Tracks")
tab1, tab2, tab3 = st.tabs(["Clustering", "Radar Plot of Clusters", "Other Plots"])

# Define data
df = st.session_state.df

# TAB1
# CLUSTERING
with tab1:
    with st.form("Clustering parameters"):
        # User defined-features and number of clusters
        st.write("Please choose at least 5 features.")
        cluster_features = st.multiselect(label="Select features to use in clustering:",
                                          options=feature_cols,
                                          default=visual_cols)
        df = df[cluster_features]
        n_clusters = st.select_slider(label="Select number of clusters:",
                                      options=range(3, 10),
                                      value=5)
        submitted_cluster = st.form_submit_button("Go!")
        df_centroids = pd.DataFrame()
        if submitted_cluster:
            # Perform K-means clustering
            # Scale any features if necessary
            for feature in cluster_features:
                if feature not in visual_cols:
                    df[feature] = minmax_scale(df[[feature]])

            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(df)
            cluster_labels = kmeans.labels_
            df_clustered = df
            df_clustered["cluster"] = cluster_labels

            # Calculate the centroid values for each cluster
            centroids = kmeans.cluster_centers_
            df_centroids = pd.DataFrame(centroids, columns=df.columns[:-1])

            # Add clustering results to session state
            st.session_state.cluster_labels = cluster_labels
            st.session_state.df_centroids = df_centroids
            st.session_state.df_clustered = df_clustered

            st.success("Clustering done!")

# TAB2
# RADAR PLOT OF FEATURES IN CLUSTER
with tab2:
    st.subheader("Radar plot of features in each cluster")
    # Create the radar chart
    selected_clusters = st.multiselect(label="Select clusters to plot:",
                                       options=range(n_clusters),
                                       default=[0, 1, 2])
    selected_features = st.multiselect(label="Select features to plot:",
                                       options=cluster_features,
                                       default=cluster_features[0:5])
    if "df_clustered" in st.session_state:
        df_clustered = st.session_state.df_clustered
        df_mean = df_clustered.groupby("cluster").mean().reset_index()

        fig = go.Figure()
        cluster_colors = pc.qualitative.Plotly[:n_clusters]
        max_value = df_mean[selected_features].max().max()  # Calculate the maximum value across selected features

        for i in selected_clusters:
            centroid_values = df_mean[df_mean["cluster"] == i][selected_features].values.flatten().tolist()
            fig.add_trace(go.Scatterpolar(
                r=centroid_values + [centroid_values[0]],
                theta=selected_features + [selected_features[0]],
                opacity=0.6,
                fill="toself",
                name=f"Cluster {i}",
                fillcolor=cluster_colors[i],
                line=dict(color='rgba(0,0,0,0)')
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max_value])),
            showlegend=True
        )
        fig.update_layout(height=600, width=800)
        # Plotly chart
        st.plotly_chart(fig)
    else:
        st.error("Please run or re-run clustering again.")

# TAB3
# BAR PLOTS OF FEATURES BY CLUSTERS
with tab3:
    selected_columns = st.multiselect(label="Select columns to plot:",
                                      options=cluster_features,
                                      default=cluster_features)
    if "df_clustered" in st.session_state:
        df_clustered = st.session_state.df_clustered
        df_mean = df_clustered.groupby("cluster").mean().reset_index()

        # Define the color palette and facet grids for subplots
        colors = pc.qualitative.Plotly
        num_plots = len(selected_columns)
        num_rows = (num_plots + 2) // 3

        fig = sp.make_subplots(rows=num_rows, cols=3, subplot_titles=selected_columns)

        for i, column in enumerate(selected_columns):
            row = i // 3 + 1
            col = i % 3 + 1

            for _, row_data in df_mean.iterrows():
                cluster = int(row_data['cluster'])
                fig.add_trace(go.Bar(
                    x=[cluster],
                    y=[row_data[column]],
                    name=f'Cluster {cluster}',
                    marker=dict(color=colors[cluster])
                ), row=row, col=col)

        fig.update_layout(
            title_text="Average of Columns by Cluster",
            grid=dict(rows=num_rows, columns=3),
            height=500 * num_rows,
            showlegend=False,
            margin=dict(l=20, r=20, t=60, b=50),
            width=1000
        )
        fig.update_xaxes(title_text="Cluster", row=num_rows, col=1)
        for i, column in enumerate(selected_columns):
            row = i // 3 + 1
            col = i % 3 + 1

            fig.update_xaxes(title_text="Cluster", row=row, col=col)
            fig.update_yaxes(title_text=column, row=row, col=col)

        st.plotly_chart(fig)
    else:
        st.error("Please run or re-run clustering again.")
