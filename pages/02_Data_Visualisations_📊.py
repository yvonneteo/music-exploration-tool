"""
Visualisations (Music Exploration Tool)
Author: Yvonne Teo
Description: This script deals with the visualisations of the data.
"""

# IMPORTS
import streamlit as st
import plotly.colors as pc
import plotly.graph_objects as go

from methods import feature_cols, visual_cols


# Page and app config
st.set_page_config(page_title="Music Exploration Tool - Data Visualisations", page_icon="🎵",  layout="wide")
st.title("Visualisations of Spotify Playlist")
tab1, tab2, tab3 = st.tabs(["Line Polar Plot of Features", "Histogram Distribution Plots", "Box Plots of Features"])

# Define data
df = st.session_state.df

# TAB1
# LINE POLAR PLOT OF FEATURES
with tab1:
    st.write("### Line Polar Plot of Features")
    df_1 = df[visual_cols + ["name"]]
    # Filter the dataframe for the selected rows
    selected_rows = st.multiselect(label="Select tracks to include:",
                                   options=df_1["name"].tolist(),
                                   default=df_1["name"].tolist()[0])
    filtered_rows = df_1[df_1["name"].isin(selected_rows)]

    # Filter the dataframe for the selected features
    selected_features = st.multiselect(label="Select features to include:",
                                       options=visual_cols,
                                       default=visual_cols)
    filtered_rows = filtered_rows[selected_features + ["name"]]

    # Create a list of traces for each selected row
    traces = []
    for _, row in filtered_rows.iterrows():
        feature_names = filtered_rows.columns[1:]
        feature_values = row.values[1:]
        feature_values = list(feature_values) + [feature_values[0]]
        trace = go.Scatterpolar(
            r=feature_values,
            theta=feature_names,
            fill='toself',
            opacity=0.5,
            hovertext=[row["name"]] * len(feature_names)
        )
        traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
    fig.update_layout(height=600, width=800)
    st.plotly_chart(fig, use_container_width=True)


# TAB2
# HISTOGRAM DISTRIBUTION PLOTS
with tab2:
    st.write("### Histogram")
    df_2 = df[feature_cols]
    # Select columns to include in the plot
    selected_columns = st.multiselect(label="Select columns to include:",
                                      options=feature_cols,
                                      default=visual_cols,
                                      key="data_v_tab_2")
    # Filter the DataFrame for the selected columns
    filtered_df = df_2[selected_columns]
    # Create traces for each selected column
    traces = []
    for column in filtered_df.columns:
        # Create the histogram trace for the current column
        trace = go.Histogram(x=filtered_df[column], opacity=0.7, name=column)
        traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(barmode='overlay',
                      bargap=0.1,
                      xaxis=dict(title='Value', title_font=dict(size=14)),
                      yaxis=dict(title='Frequency', title_font=dict(size=14))
                      )
    st.plotly_chart(fig, use_container_width=True)

# TAB3
# BOX PLOTS
with tab3:
    st.write("### Box Plot of Features")
    df_3 = df[feature_cols]
    # Select columns to include in the plot
    selected_features = st.multiselect(label="Select columns to include:",
                                       options=feature_cols,
                                       default=visual_cols[:10],
                                       max_selections=10,
                                       key="data_v_tab_3")
    # Filter the DataFrame for the selected columns
    filtered_data = df_3[selected_features]

    # Create the box plots
    fig = go.Figure()
    colors = pc.qualitative.Plotly[:len(selected_features)]

    for i, feature in enumerate(filtered_data[selected_features]):
        fig.add_trace(go.Box(y=filtered_data[feature],
                             name=feature,
                             boxpoints="all",
                             jitter=0.3,
                             marker_color=colors[i]))
    fig.update_layout(title="Box Plots of Selected Features",
                      yaxis_title="Feature",
                      xaxis_title="Value",
                      violinmode="group",
                      showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
