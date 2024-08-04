import pandas as pd
import logging
from mysql.connector import Error
from src.mysql_db.mysql_connection import MySQLConnectionSingleton

class DatabaseManager:
    def __init__(self):
        self.db_instance = MySQLConnectionSingleton()
        self.mycursor = self.db_instance.connectDB_get_cursor()
        self.engine = self.db_instance.get_mysql_engine()
        
    def _check_connection(self):
        if not self.db_instance._connection.is_connected():
            logging.info("Reconnecting to the database.")
            self.db_instance = MySQLConnectionSingleton()
            self.mycursor = self.db_instance.connectDB_get_cursor(buffered=True)
            self.engine = self.db_instance.get_mysql_engine()
        else:
            logging.info("Connection is active.")     

    def create_tables(self):
        try:
            self._check_connection()
            self.mycursor.execute('''CREATE TABLE IF NOT EXISTS channel( 
                                    channel_name VARCHAR(100),
                                    channel_id VARCHAR(50) PRIMARY KEY,
                                    channel_Description VARCHAR(1000),
                                    channel_Thumbnail VARCHAR(255),
                                    channel_playlist_id VARCHAR(50),
                                    channel_subscribers BIGINT,
                                    channel_video_count BIGINT,
                                    channel_views BIGINT,
                                    channel_publishedate DATETIME)''')

            self.mycursor.execute('''CREATE TABLE IF NOT EXISTS playlist(
                                    playlist_id VARCHAR(50) PRIMARY KEY,
                                    playlist_name VARCHAR(100),
                                    publishedat DATETIME,
                                    channel_id VARCHAR(50),
                                    channel_name VARCHAR(100),
                                    videoscount BIGINT)''')

            self.mycursor.execute('''CREATE TABLE IF NOT EXISTS videos(
                                    channel_id VARCHAR(50),
                                    video_id VARCHAR(50) PRIMARY KEY,
                                    video_name VARCHAR(100),
                                    video_Description VARCHAR(1000),
                                    Thumbnail VARCHAR(100),
                                    Tags VARCHAR(1000),
                                    publishedAt DATETIME,
                                    Duration VARCHAR(10),
                                    View_Count BIGINT,
                                    Like_Count BIGINT,
                                    Favorite_Count BIGINT,
                                    Comment_Count BIGINT,
                                    Caption_Status VARCHAR(10),
                                    FOREIGN KEY (channel_id) REFERENCES channel(channel_id))''')

            self.mycursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                                    video_id VARCHAR(50),
                                    comment_id VARCHAR(50),
                                    comment_text TEXT,
                                    comment_author VARCHAR(50),
                                    comment_publishedat DATETIME,
                                    FOREIGN KEY (video_id) REFERENCES videos(video_id))''')
            print("Tables created successfully.")
        except Error as e:
            logging.error(f"Error creating tables: {e}")
            raise
    
    def upload_data(self, df, table_name):
        try:
            self._check_connection()
            if table_name == "videos":
                df['Tags'] = df['Tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            self.db_instance._connection.commit()
            print(f'Data uploaded successfully to {table_name}.')
        except Exception as e:
            logging.warning(f"Exception Name: {type(e).__name__}")
            logging.warning(f"Exception Desc: {e}")
            raise

    def fetch_channel_names(self):
        try:
            self._check_connection()  # Ensure the connection is active
            self.mycursor.execute("SELECT channel_name FROM channel")
            channel_names = [row[0] for row in self.mycursor.fetchall()]
            return channel_names
        except Error as e:
            logging.error(f"Error fetching channel names: {e}")
            return []

    def load_channel_data(self, channel_name):
        try:
            self._check_connection()  # Ensure the connection is active

            # Fetch channel data
            self.mycursor.execute("SELECT * FROM channel WHERE channel_name = %s", (channel_name,))
            channel_rows = self.mycursor.fetchall()
            channel_df = pd.DataFrame(channel_rows, columns=[i[0] for i in self.mycursor.description]).reset_index(drop=True)
            channel_df.index += 1

            # Fetch playlists data
            self.mycursor.execute("SELECT * FROM playlist WHERE channel_id = %s", (channel_df['channel_id'].iloc[0],))
            playlist_rows = self.mycursor.fetchall()
            playlists_df = pd.DataFrame(playlist_rows, columns=[i[0] for i in self.mycursor.description]).reset_index(drop=True)
            playlists_df.index += 1

            # Fetch videos data
            self.mycursor.execute("SELECT * FROM videos WHERE channel_id = %s", (channel_df['channel_id'].iloc[0],))
            video_rows = self.mycursor.fetchall()
            videos_df = pd.DataFrame(video_rows, columns=[i[0] for i in self.mycursor.description]).reset_index(drop=True)
            videos_df.index += 1

            # Fetch comments data
            self.mycursor.execute("SELECT * FROM comments WHERE video_id IN (SELECT video_id FROM videos WHERE channel_id = %s)",
                           (channel_df['channel_id'].iloc[0],))
            comment_rows = self.mycursor.fetchall()
            comments_df = pd.DataFrame(comment_rows, columns=[i[0] for i in self.mycursor.description]).reset_index(drop=True)
            comments_df.index += 1

            return channel_df, playlists_df, videos_df, comments_df
        except Error as e:
            logging.error(f"Error loading channel data: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
    # Query methods
    def sql_question_1(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name,videos.video_name
                                    FROM videos 
                                    JOIN channel ON channel.channel_id = videos.channel_id
                                    ORDER BY channel_name''')
            out = self.mycursor.fetchall()
            Q1 = pd.DataFrame(out, columns=['Channel Name', 'Videos Name']).reset_index(drop=True)
            Q1.index += 1
            return Q1
        except Error as e:
            logging.error(f"Error fetching data for question 1: {e}")
            return []
        
    def sql_question_2(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT DISTINCT channel_name, COUNT(videos.video_id) as Total_Videos 
                                    FROM channel 
                                    JOIN videos ON channel.channel_id = videos.channel_id
                                    GROUP BY channel_name 
                                    ORDER BY Total_videos DESC''')
            out = self.mycursor.fetchall()
            Q2 = pd.DataFrame(out, columns=['Channel Name', 'Total Videos']).reset_index(drop=True)
            Q2.index += 1
            return Q2
        except Error as e:
            logging.error(f"Error fetching data for question 2: {e}")
            return []

    def sql_question_3(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name, videos.video_name, videos.view_count as Total_Views
                                    FROM videos
                                    JOIN channel ON channel.channel_id = videos.channel_id
                                    ORDER BY videos.view_count DESC
                                    LIMIT 10''')
            out = self.mycursor.fetchall()
            Q3 = pd.DataFrame(out, columns=['Channel Name', 'Videos Name', 'Total Views']).reset_index(drop=True)
            Q3.index += 1
            return Q3
        except Error as e:
            logging.error(f"Error fetching data for question 3: {e}")
            return []

    def sql_question_4(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT videos.video_name, videos.comment_count as Total_Comments
                                    FROM videos
                                    ORDER BY videos.comment_count DESC''')
            out = self.mycursor.fetchall()
            Q4 = pd.DataFrame(out, columns=['Videos Name', 'Total Comments']).reset_index(drop=True)
            Q4.index += 1
            return Q4
        except Error as e:
            logging.error(f"Error fetching data for question 4 : {e}")
            return []

    def sql_question_5(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name, videos.video_name, videos.like_count as Highest_likes 
                                    FROM videos 
                                    JOIN channel ON videos.channel_id = channel.channel_id
                                    WHERE like_count = (SELECT MAX(videos.like_count) 
                                                        FROM videos v 
                                                        WHERE videos.channel_id = v.channel_id
                                                        GROUP BY channel_id)
                                    ORDER BY Highest_likes DESC''')
            out = self.mycursor.fetchall()
            Q5 = pd.DataFrame(out, columns=['Channel Name', 'Videos Name', 'Likes']).reset_index(drop=True)
            Q5.index += 1
            return Q5
        except Error as e:
            logging.error(f"Error fetching data for question 5 : {e}")
            return []

    def sql_question_6(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT videos.video_name, videos.like_count as Likes
                                    FROM videos
                                    ORDER BY videos.like_count DESC''')
            out = self.mycursor.fetchall()
            Q6 = pd.DataFrame(out, columns=['Videos Name', 'Likes']).reset_index(drop=True)
            Q6.index += 1
            return Q6
        except Error as e:
            logging.error(f"Error fetching data for question 6 : {e}")
            return []

    def sql_question_7(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name, channel.channel_views as Total_views
                                    FROM channel
                                    ORDER BY channel.channel_views DESC''')
            out = self.mycursor.fetchall()
            Q7 = pd.DataFrame(out, columns=['Channel Name', 'Total views']).reset_index(drop=True)
            Q7.index += 1
            return Q7
        except Error as e:
            logging.error(f"Error fetching data for question 7 : {e}")
            return []

    def sql_question_8(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT DISTINCT channel.channel_name
                                    FROM channel
                                    JOIN videos ON videos.channel_id = channel.channel_id
                                    WHERE YEAR(videos.publishedAt) = 2022''')
            out = self.mycursor.fetchall()
            Q8 = pd.DataFrame(out, columns=['Channel Name']).reset_index(drop=True)
            Q8.index += 1
            return Q8
        except Error as e:
            logging.error(f"Error fetching data for question 8 : {e}")
            return []

    def sql_question_9(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name,
                                            TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.Duration)))), "%H:%i:%s") AS Duration
                                    FROM videos
                                    JOIN channel ON videos.channel_id = channel.channel_id
                                    GROUP BY channel_name''')
            out = self.mycursor.fetchall()
            Q9 = pd.DataFrame(out, columns=['Channel Name', 'Duration']).reset_index(drop=True)
            Q9.index += 1
            return Q9
        except Error as e:
            logging.error(f"Error fetching data for question 9 : {e}")
            return []

    def sql_question_10(self):
        try:
            self._check_connection()
            self.mycursor.execute('''SELECT channel.channel_name, videos.video_name, videos.comment_count as Total_Comments
                                    FROM videos
                                    JOIN channel ON channel.channel_id = videos.channel_id
                                    ORDER BY videos.comment_count DESC''')
            out = self.mycursor.fetchall()
            Q10 = pd.DataFrame(out, columns=['Channel Name', 'Videos Name', 'Comments']).reset_index(drop=True)
            Q10.index += 1
            return Q10
        except Error as e:
            logging.error(f"Error fetching data for question 10 : {e}")
            return []
        
    def plot_channels_subscribers(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT channel_name, channel_subscribers 
                                    FROM channel
                                    ORDER BY channel_subscribers DESC''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Channel Name', 'Subscribers Count'])
            return df
        except Error as e:
            logging.error(f"Error fetching channel subscribers: {e}")
            return pd.DataFrame()

    def plot_channels_videos(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT channel_name, channel_video_count AS Total_Videos
                                    FROM channel 
                                    ORDER BY channel_video_count DESC''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Channel Name', 'Total Videos'])
            return df
        except Error as e:
            logging.error(f"Error fetching channel videos: {e}")
            return pd.DataFrame()

    def plot_top_10_viewed_videos(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT channel.channel_name, videos.video_name, videos.view_count AS Total_Views
                                    FROM videos
                                    JOIN channel ON channel.channel_id = videos.channel_id
                                    ORDER BY videos.view_count DESC
                                    LIMIT 10''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Channel Name', 'Video Name', 'Total Views'])
            return df
        except Error as e:
            logging.error(f"Error fetching top 10 viewed videos: {e}")
            return pd.DataFrame()

    def plot_channels_total_views(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT channel_name, channel_views AS Total_Views
                                    FROM channel
                                    ORDER BY channel_views DESC''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Channel Name', 'Total Views'])
            return df
        except Error as e:
            logging.error(f"Error fetching total views: {e}")
            return pd.DataFrame()

    def plot_channels_average_duration(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT channel.channel_name,
                                    TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(videos.duration)))), "%H:%i:%s") AS Duration
                                    FROM videos
                                    JOIN channel ON videos.channel_id = channel.channel_id
                                    GROUP BY channel_name ORDER BY Duration ASC''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Channel Name', 'Average Duration'])
            return df
        except Error as e:
            logging.error(f"Error fetching average video duration: {e}")
            return pd.DataFrame()

    def plot_yearwise_performance(self):
        self._check_connection()
        try:
            self.mycursor.execute('''SELECT DISTINCT YEAR(videos.publishedAt) AS Years, COUNT(videos.video_id) AS Total_Videos,
                                    SUM(videos.like_count) AS Total_Likes, SUM(videos.view_count) AS Total_Views, 
                                    SUM(videos.comment_count) AS Total_Comments, channel.channel_name
                                    FROM videos 
                                    LEFT JOIN channel ON videos.channel_id = channel.channel_id 
                                    GROUP BY channel_name, Years''')
            data = self.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Years', 'Total Videos', 'Likes', 'Views', 'Total Comments', 'Channel Name'])
            return df
        except Error as e:
            logging.error(f"Error fetching year-wise performance: {e}")
            return pd.DataFrame()                 

    def close(self):
        if self.db_instance._connection.is_connected():
            self.db_instance.close()

# Ensure only one instance globally
database_manager_instance = DatabaseManager()
