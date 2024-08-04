import streamlit as st
import pandas as pd
import logging
from src.api.youtube_api import youtube_api_instance
from src.mysql_db.mysql_db_request import database_manager_instance

# Initialize YouTubeAPI and MySQL singleton class instances
youtube_api = youtube_api_instance
db_manager = database_manager_instance

# Function to display a colored subheader
def colored_subheader(text, color):
    st.markdown(f"<h3 style='color:{color};'>{text}</h3>", unsafe_allow_html=True)

# Page Title
st.title(':red[YouTube Data Collection and MySQL Upload]')

# Data collection and upload section
colored_subheader('Data Collection and Upload', 'blue')

st.markdown('''
    - Provide the channel ID in the input field.
    - Clicking the 'View Details' button will display an overview of the YouTube channel.
    - Clicking 'Upload to MYSQL database' will store the extracted channel information,
      playlists, videos, and comments in a MySQL Database.
''')

st.markdown('''
    :red[note:] ***You can get the channel ID:***
    Open YouTube - go to any channel - go to About - Share channel - copy the channel ID
''')

# Input for channel ID
channel_ID = st.text_input("**Enter the channel ID in the below box:**")

# Validate channel ID input
if st.button("View Details"):
    if not channel_ID.strip():
        st.error("Channel ID cannot be empty. Please enter a valid channel ID.")
    else:
        with st.spinner('Extraction in progress...'):
            try:
                st.write("Calling API...")
                extracted_details = youtube_api.channel_information(channel_ID)
                
                if extracted_details:
                    st.write('**:blue[Channel Thumbnail]**:')
                    st.image(extracted_details.get('channel_Thumbnail', 'https://via.placeholder.com/150'), width=150)
                    st.write('**:blue[Channel Name]**:', extracted_details.get('channel_name', 'N/A'))
                    st.write('**:blue[Description]**:', extracted_details.get('channel_Description', 'N/A'))
                    st.write('**:blue[Total Videos]**:', extracted_details.get('channel_video_count', 'N/A'))
                    st.write('**:blue[Subscriber Count]**:', extracted_details.get('channel_subscribers', 'N/A'))
                    st.write('**:blue[Total Views]**:', extracted_details.get('channel_views', 'N/A'))
                else:
                    st.warning("No details found for the given channel ID.")
                
            except RuntimeError as e:
                st.error(f"API error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if st.button("Upload to MYSQL database"):
    if not channel_ID.strip():
        st.error("Channel ID cannot be empty. Please enter a valid channel ID.")
    else:
        with st.spinner('Upload in progress...'):
            try:
                # Create tables in the SQL database
                db_manager.create_tables()
                
                # Transform corresponding data into pandas dataframes
                df_channel = pd.DataFrame([youtube_api.channel_information(channel_ID)])
                df_playlist = pd.DataFrame(youtube_api.playlist_information(channel_ID))
                video_ids = youtube_api.get_video_ids(channel_ID)
                df_videos = pd.DataFrame(youtube_api.video_information(video_IDS=video_ids))
                df_comments = pd.DataFrame(youtube_api.comments_information(video_IDS=video_ids))
                
                # Ensure each dataframe is checked and uploaded if not empty
                if not df_channel.empty:
                    db_manager.upload_data(df_channel, table_name="channel")
                if not df_playlist.empty:
                    db_manager.upload_data(df_playlist, table_name="playlist")
                if not df_videos.empty:
                    db_manager.upload_data(df_videos, table_name="videos")
                if not df_comments.empty:
                    db_manager.upload_data(df_comments, table_name="comments")
                
                # Check if at least one dataframe is uploaded successfully
                if not df_channel.empty or not df_playlist.empty or not df_videos.empty or not df_comments.empty:
                    st.success('Channel information, playlists, videos, comments are uploaded successfully.')
                else:
                    st.warning('No data retrieved to upload. Please check the channel ID and try again.')
                
            except Exception as e:
                logging.warning(f"Exception Name: {type(e).__name__}")
                logging.warning(f"Exception Desc: {e}")
                st.error('Failed to upload data to MYSQL database. Check logs for details.')

          
            
                

    