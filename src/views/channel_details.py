import streamlit as st
import pandas as pd
import logging
from src.api.youtube_api import youtube_api_instance
from src.mysql_db.mysql_db_request import database_manager_instance

# Initialize YouTubeAPI and MySQL singleton class instances
youtube_api = youtube_api_instance
db_manager = database_manager_instance


if True:
    st.subheader(':blue[MySQL Database]')
    st.markdown('''__You can view the channel details along with the playlist,videos,comments in table format 
                    which is stored in MYSQL database__''')
    try:
        channel_names = db_manager.fetch_channel_names()
        selected_channel = st.selectbox(':red[Select Channel]', channel_names) 
    
        if selected_channel:
            channel_info,playlist_info,videos_info,comments_info = db_manager.load_channel_data(selected_channel)

        st.subheader(':blue[Channel Table]')
        st.write(channel_info)
        st.subheader(':blue[Playlists Table]')
        st.write(playlist_info)
        st.subheader(':blue[Videos Table]')
        st.write(videos_info)
        st.subheader(':blue[Comments Table]')
        st.write(comments_info)
    except BaseException as exception:
        st.error('Database is empty ')
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}") 
