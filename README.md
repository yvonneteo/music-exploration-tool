# Music Exploration Tool
A music exploration tool using Spotify playlists

## Introduction
The goal of this project was to build a working prototype of a music exploration tool in Python, using the framework provided by Streamlit to create a web app helping composers explore features of music that may otherwise be difficult to access in a meaningful way. In this report, I will cover the following areas of interest regarding the project:
1. How to use the program
2. The development process
3. Challenges 
4. Future work and conclusion

## How to use the Music Exploration Tool
The music exploration tool is built on Streamlit, a Python library module that allows users to create web applications, primarily based around data. By the end of the project, the music exploration tool consisted of four main parts, corresponding to a page on the web app:
1. importing data, 
2. displaying data (as a dataframe) and providing an interface for user input to enhance data, 
3. data visualisations (in the form of charts and plots), and finally, 
4. unsupervised clustering done on the data with relevant visualisations of clustering.
   
In this section, the steps to use the music exploration tool will be detailed.
### Steps to use the Music Exploration Tool
#### Setting up
There are two ways to set up the environment for the music exploration tool. This assumes that the user already has Python installed. 
##### Manual pip installation:  
(This assumes the user has pip installed. Otherwise, there is a quick tutorial in the Appendix pertaining to steps for installing pip.)  
Using the command pip install [dependency] in the terminal, install all the dependencies listed in the appendix.  
Once all the dependencies have been installed, run:  `streamlit run Music_Exploration_Tool_🎵.py `
##### Poetry installation: 
Install Poetry according to the documentation provided by the developers of Poetry. A guide is provided in the Appendix. This would differ depending on the operating system.  There are already files that Poetry needs to run in the project deliverables, which detail the dependencies and versions that are needed for the music exploration tool. To install these files, in the terminal, run: 
`poetry install`  
Once all the dependencies have been installed, run: `poetry run streamlit run Music_Exploration_Tool_🎵.py`

#### Importing data
The web app should have popped up in the default browser. In order to run the web app successfully, data has to be imported. 
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/2fb99f9d-dfb9-4239-8d6d-badb3d6794df)
This can be done in two ways:
##### Importing data from directory: 
The default option is to import a pickled dataset from the directory, by defining a file path from which the dataset would be loaded. A sample master dataset is provided, and the path to it is the default value. To import this dataset, simply click the “Import data” button at the end of the form.  Alternatively, if there are specific datasets in the .pkl format, one can be loaded by inputting the file path in the field “File path for dataframe”, then clicking the “Import data” button.
##### Fetching new data from Spotify API: 
Alternatively, new data can be fetched from the Spotify API. Select “No, fetch new data from Spotify API” at the top, then input relevant Spotify API settings. There are default values here as one would need to go through the process of creating a Spotify Developer account and a client ID to get the Spotify CID and Spotify User Secret otherwise. This can be done by following the instructions at this tutorial and the default values can be replaced.  Next, copy the URL to the desired Spotify playlist and paste it in the “Playlist ID or URL” field, then click “Import data”.  This creates a new pickled dataset in the directory and adds data from the playlist to the master dataset.
A success message that reads “Data imported successfully!” should pop up when data has been imported. If an error or exception message pops up, check the relevant fields and try again.
When the “Import data” button is clicked, the master dataset is always updated.

#### Displaying data
After data has been imported, click on the “Data 💡” page on the sidebar, which will load a page with an editable dataframe. 
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/7c091496-dff8-4f5d-8555-a2d622c28179)


#### Editing data
One can edit or add data by double-clicking on the desired cell and inputting any new value. 
Alternatively, the “Add moods to dataframe” form at the bottom of the page allows the user to choose and input moods from a dropdown box for a selected track, which may be useful in certain use cases, and add notes together along with it. 
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/62cc7f56-59f4-4a08-8ab9-8b6151c41304)


#### Other functionality
The “Reload data” button reloads the data so that any changes made to the data will be shown. The “Save data” button saves a new copy of the data after a user has made all the changes desired and wants to save a copy of the edited data. 
Finally, the “Add clusters” button adds the clusters from the unsupervised clustering to the dataframe. A user could then potentially sort tracks based on the cluster it belongs to and glean insights.

#### Data visualisations 📊
There are three tabs under the Data Visualisations page, each customised and using Plotly to create interactive visualisations that can be downloaded as a PNG natively in Plotly.
#### Line Polar Plot of Features
The first tab shows a line polar plot of features per track, where the features shown and the corresponding track(s) can be selected by the user. The features included that are available for selection are only features that fall within the range of 0 and 1, so as to maintain a visually appropriate scale.
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/3d0b9ad2-ee52-4f1c-8061-48a454ce11c9)

### Histogram Distribution Plots
The second tab shows a histogram distribution plot of features across the entire dataset. Features can be selected by the user. The Plotly chart also has functionality for removing a “trace” or feature by clicking its name on the legend on the right, or isolating a single “trace” or feature by double-clicking. 
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/588f0781-6d3e-47e5-8bf2-8d331824b22f)

#### Box Plot of Features
The third tab shows a set of box plots for selected features across the entire dataset. The functionality is similar to that of the Histogram Distribution Plot tab.
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/4693451b-7e0e-4099-bdb9-c6e95512877c)


#### Clustering of Spotify Tracks
Unsupervised clustering, where tracks in the dataset are grouped using a machine-learning algorithm (namely k-means clustering used here with only numeric variables), can be carried out on the dataset with user-selected features and a user-defined number of clusters. 
![image](https://github.com/yvonneteo/musicexplorationtool/assets/83072865/a0c87192-e111-4691-9456-effb0cc2d3c2)


After clustering, the user may move to the second and third tabs “Radar Plot of Clusters” and “Other Plots” to explore how different clusters differ visually. 

## Development Process of Music Exploration Tool
The development process of the music exploration tool can be roughly divided into four stages:
1. Exploration of libraries and tools
2. Developing the structure of the web app
3. Programming code for data visualisations
4. Polishing user-interactivity and other functionalities in the web app
   
### 1. Exploration of libraries and tools
There are a number of libraries and tools for three major aspects of the program: Spotify API, web application, and data visualisation. Before embarking upon this project at all, it was paramount to ensure that interfacing with the Spotify API would be possible. After experimenting with different ways of interfacing with the Spotify API through Jupyter notebooks attached in the appendices, Spotipy was chosen for its ease of use. 
Although there are other web application frameworks such as Dash and Gradio, Streamlit was chosen for its gentler learning curve compared to Dash, and functionality compared to Gradio.
Finally, as downloadable charts and interactivity rather than a static plot would be important due to the complexity of the charts, Plotly was chosen over matplotlib. 

### 2. Developing the structure of the web app
The overall structure of the web app had been decided at the start of the project, where a web app with some functionality for editing the dataframe, visualising the data and carrying out unsupervised clustering was the goal. The documentation for Streamlit was extremely accessible and there was a robust community in which many issues that came up during programming with Streamlit had been resolved. It was possible to test the music exploration tool’s functionality in frequent, small increments of progress such that any problems in the code could be quickly pinpointed and resolved. 
There were some challenges that surfaced during this stage, and were eventually resolved by rethinking the structure of the web app in a way that still preserved its functionalities. 

### 3. Programming code for data visualisations
After figuring out the flow of the program, the code for data visualisations was the most challenging part of programming the music exploration tool. As Plotly’s syntax is somewhat different from matplotlib, it was challenging to figure out how to code the visualisations in a way that would be useful to the user. It took many tries and consulting code and explanations on StackOverflow, in order to finally create a subset of the visualisations intended. 

### 4. Polishing user-interactivity and other functionalities in the web app
After building up the web app and incorporating some visualisations, it was necessary to test different combinations of user selections for Streamlit widgets to ensure that the web app would not break with certain combinations. Some tweaks and minor changes were added at this stage. 


### Technical development steps
The technical steps of the development process could be visualised as follows:
1. Exploration of libraries and tools: This was done at the start of the project, and included experiments on Jupyter notebooks, as well as reading through documentation and articles about commonly-used libraries and tools.
   
   i. Different ways of interacting with Spotify API

   ii. Different web app platforms/frameworks (e.g. Streamlit, Dash, Gradio)
  
   iii. Different data visualisation libraries (e.g. Matplotlib, Seaborn, Plotly, Altair)
  
2. Building the streamlit app: Once decisions were made regarding the libraries to use, PyCharm was used with a Poetry environment to start writing a Python script. Code was then refactored into functions and moved to a methods.py file from which they were imported. This resulted in cleaner code.

   i. Coding the main page for Streamlit with the idea of using tabs

   ii. Figuring out the flow for importing data, on which the other components in the app relied, then deciding instead to use a multi-page Streamlit app

   iii. Experimenting with Streamlit components to control flow such as st.form, st.session_state, st.experimental_rerun and st.cache_data
   
3. Programming data visualisations:

   i. Using online resources like StackOverflow and Plotly documentation to figure out how to write data visualisation code
  
   ii. Lots of trials and errors
  
4. Testing app
   
   i. Testing different combinations of user selections such as different feature sets, different ways of importing data, jumping across different pages not necessarily in the order of Data, Data Visualisations and Clustering after importing data
   
   ii. Tweaking instructions and if-else conditions, adding success and error messages so that the user knows what is going on

### Challenges
#### Control Flow
The main challenge was that data had to be imported by the user in some way before components like displaying the dataframe or data visualisations could run. However, Streamlit does not offer built-in functionality for running sections of code in steps. In other words, the entire script runs when the web app is launched. Thus, when data has not been imported at the start of the run, the app throws errors where components are expecting to interact with data. 

The original intention was to use a sidebar to import and filter data, and tabs on the page for users to navigate to different aspects of the web app (e.g. data visualisations, clustering, etc.). However, this resulted in ugly error messages upon starting up the web app, so it was necessary to work around the issue. Instead of the original plan, a multi-page web app was built, coding each aspect in a separate script. The main page would then ask for the user to import data. Although the other pages would still throw errors, it would be less disruptive visually.

This brought up a problem of sharing variables like the dataset across pages and between reruns, which was resolved with the Streamlit session state, which preserves and persists the dataset imported in the main page across all the pages. Other components like reloading the data or updating the data with edits (such as adding notes or clusters) would also work now under the session state variable.

Another challenge was resolved using Streamlit’s form that batches information together before being sent to Streamlit, which would prevent Streamlit from re-running whenever a user makes a single change to a widget, as the user might in the process of making multiple changes. This made the user interface much more pleasant and cut down on processing.

### Data Visualisation
Programming with Plotly was a newer experience and thus presented a somewhat steep learning curve, but the challenge itself was straightforward—by understanding the Plotly syntax and learning through trial and error and looking through StackOverflow questions and answers, this was resolved. 
#### Embedding Spotify Player
Some attempts were made at embedding a Spotify player in the app, which would increase user functionality. However, there was a persistent issue with the embedded Spotify player consistently throwing an error of “Page not found”, with publicly available playlists and tracks. In the interest of time, this was abandoned to complete other components and ensure that they worked smoothly, but it would have been a useful function to add.  

### Future Work and Conclusion
Although the building of a prototype for a music exploration tool, primarily geared towards personal use, was generally successful, there remains work that can be done in the future to improve the tool.
Firstly, more visualisations can be added to further explore the data. Although there are some visualisations that yield insights to the music, more time could be spent on developing more sophisticated visualisations, such as correlation charts to look at how features may be correlated, as well as interaction charts to look at how two features may be correlated to each other in the dataset, specifically. 
Another area for future work could be more flexibility in how the user can add to the dataset and create plots that would be interesting to them.
Finally, it would be a useful functionality to have a Spotify player embedded so that users could listen real-time to any track they may have had specific interest in or questions about. 
In conclusion, this was in general a successful project, as a music exploration tool web-app was successfully built, with most of the functionality aimed for in an earlier Statement of Interest, which can be found in the appendices. However, certain aspects such as data visualisation and general user functionality could be improved in the future. Appendices


### Appendix: Tutorials and Documentation
Tutorial for installing pip:
https://phoenixnap.com/kb/install-pip-mac
https://phoenixnap.com/kb/install-pip-windows

Tutorial for installing poetry:
https://python-poetry.org/docs/
https://realpython.com/dependency-management-python-poetry/#python-poetry-installation

Tutorial for getting started with Spotify API: (To get Spotify CLI and User Secret)
https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b

Streamlit Documentation:
https://docs.streamlit.io/

Plotly Documentation:
https://plotly.com/python/
https://plotly.com/python/graph-objects/
