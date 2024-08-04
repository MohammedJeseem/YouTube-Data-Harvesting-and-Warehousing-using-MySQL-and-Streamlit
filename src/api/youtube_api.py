
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import configparser
import streamlit as st
import re
from src.utils.date_convert_to_mysql import convert_date_format_to_store_sql,parse_datetime
from src.utils.convert_duration import convert_duration

# Read API configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

api_service_name = config['youtubeAPI']['api_service_name']
api_version = config['youtubeAPI']['api_version']
api_Key = config['youtubeAPI']['api_Key']

class YouTubeAPI:
    def __init__(self):
        self.youtube_service_instance = None

    def get_youtube_service(self):
        if self.youtube_service_instance is None:
            print("Creating new YouTube service instance...")
            self.youtube_service_instance = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_Key)
        else:
            print("Reusing existing YouTube service instance...")
        return self.youtube_service_instance

    def channel_information(self, channel_id):
        youtube = self.get_youtube_service()
        try:
            print("Requesting API for channel information")
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
            response = request.execute()
            for i in response['items']:
                mysql_datetime_str = parse_datetime(i['snippet']['publishedAt'])
                channel_data = {
                    'channel_name': i['snippet']['title'],
                    'Channel_id': i["id"],
                    'channel_Description': i['snippet']['description'],
                    'channel_Thumbnail': i['snippet']['thumbnails']['default']['url'],
                    'channel_playlist_id': i['contentDetails']['relatedPlaylists']['uploads'],
                    'channel_subscribers': i['statistics']['subscriberCount'],
                    'channel_video_count': i['statistics']['videoCount'],
                    'channel_views': i['statistics']['viewCount'],
                    'channel_publishedate': mysql_datetime_str
                }
            return channel_data
        except HttpError as e:
            if e.resp.status == 403 and e.error_details[0]["reason"] == 'quotaExceeded':
                raise RuntimeError("API Quota exceeded. Please try again later.")
            else:
                raise RuntimeError("Failed to fetch channel information.")

    def playlist_information(self, channel_id):
        youtube = self.get_youtube_service()
        playlist_info = []
        nextPageToken = None
        try:
            while True:
                request = youtube.playlists().list(
                    part="snippet,contentDetails",
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=nextPageToken
                )
                response = request.execute()

                for i in response['items']:
                    mysql_datetime_str = parse_datetime(i['snippet']['publishedAt'])
                    data = dict(
                        playlist_id=i['id'],
                        playlist_name=i['snippet']['title'],
                        publishedat=mysql_datetime_str,
                        channel_ID=i['snippet']['channelId'],
                        channel_name=i['snippet']['channelTitle'],
                        videoscount=i['contentDetails']['itemCount']
                    )
                    playlist_info.append(data)
                    nextPageToken = response.get('nextPageToken')
                if nextPageToken is None:
                    break
        except HttpError as e:
            error_message = f"Error retrieving playlists: {e}"
            st.error(error_message)
        return playlist_info

    def get_video_ids(self, channel_id):
        youtube = self.get_youtube_service()
        response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
        playlist_videos = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        next_page_token = None
        videos_ids = []

        while True:
            response1 = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_videos,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for i in range(len(response1['items'])):
                videos_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token = response1.get('nextPageToken')

            if next_page_token is None:
                break
        return videos_ids

    def video_information(self, video_IDS):
        youtube = self.get_youtube_service()
        video_info = []
        for video_id in video_IDS:
            response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            ).execute()

            for i in response['items']:
                mysql_datetime_str = parse_datetime(i['snippet']['publishedAt'])
                data = dict(
                    channel_id=i['snippet']['channelId'],
                    video_id=i['id'],
                    video_name=i['snippet']['title'],
                    video_Description=i['snippet']['description'],
                    Thumbnail=i['snippet']['thumbnails']['default']['url'],
                    Tags=i['snippet'].get('tags'),
                    publishedAt=mysql_datetime_str,
                    Duration= convert_duration(i['contentDetails']['duration']),
                    View_Count=i['statistics']['viewCount'],
                    Like_Count=i['statistics'].get('likeCount', 0),
                    Favorite_Count=i['statistics'].get('favoriteCount', 0),
                    Comment_Count=i['statistics'].get('commentCount', 0),
                    Caption_Status=i['contentDetails']['caption']
                )
                video_info.append(data)
        return video_info
    
    # def comments_information(self, video_IDS):
    #     youtube = self.get_youtube_service()
    #     comments_info = []
    #     disabled_comments_videos = []  # To store videos with disabled comments
    #     for video_id in video_IDS:
    #         try:
    #             request = youtube.commentThreads().list(
    #                 part="snippet",
    #                 videoId=video_id,
    #                 maxResults=100
    #             )
    #             response = request.execute()

    #             for i in response.get('items', []):
    #                 mysql_datetime_str = parse_datetime(i['snippet']['topLevelComment']['snippet']['publishedAt'])
    #                 data = dict(
    #                     video_id=i['snippet']['videoId'],
    #                     comment_id=i['snippet']['topLevelComment']['id'],
    #                     comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
    #                     comment_author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
    #                     comment_publishedat=mysql_datetime_str
    #                 )
    #                 comments_info.append(data)
    #         except HttpError as e:
    #             if e.resp.status == 403 and 'commentsDisabled' in str(e):
    #                 disabled_comments_videos.append(video_id)
    #             else:
    #                 st.error(f"An error occurred for video ID {video_id}: {e}")

    #     # Log or handle the list of videos with disabled comments
    #     if disabled_comments_videos:
    #         st.warning(f"Comments are disabled for the following video IDs: {disabled_comments_videos}")

    #     return comments_info
    
    
    def comments_information(self, video_IDS):
        youtube = self.get_youtube_service()
        comments_info = []
        disabled_comments_videos = []  # To store videos with disabled comments

        for video_id in video_IDS:
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100
                )
                response = request.execute()

                for i in response.get('items', []):
                    mysql_datetime_str = parse_datetime(i['snippet']['topLevelComment']['snippet']['publishedAt'])
                    data = dict(
                        video_id=i['snippet']['videoId'],
                        comment_id=i['snippet']['topLevelComment']['id'],
                        comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                        comment_author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        comment_publishedat=mysql_datetime_str
                    )
                    comments_info.append(data)
            except HttpError as e:
                if e.resp.status == 403 and 'commentsDisabled' in str(e):
                    if video_id not in disabled_comments_videos:
                        disabled_comments_videos.append(video_id)
                        st.warning(f"Comments are disabled for video ID {video_id}")
                else:
                    st.error(f"An error occurred for video ID {video_id}: {e}")
                    
                if len(disabled_comments_videos) >= 5:
                    st.warning("Stopping process due to too many videos with disabled comments.")
                    return comments_info  # Return the collected comments information if threshold is reached
                continue

        # Log the total number of videos with disabled comments
        if disabled_comments_videos:
            st.warning(f"Total videos with disabled comments: {len(disabled_comments_videos)}")

        return comments_info
        
# Ensure only one instance globally
youtube_api_instance = YouTubeAPI()    