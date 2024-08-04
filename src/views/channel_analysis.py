import streamlit as st
from src.mysql_db.mysql_db_request import database_manager_instance

# Initialize MySQL singleton class instances
db_manager = database_manager_instance


# Setting up the option "Analysis using SQL" in streamlit page 
if True:
    st.subheader(':blue[Analysis using MySQL]')
    st.markdown('''You can analyze the collection of YouTube channel data stored in a MySQL database.
                Based on selecting the listed questions below, the output will be displayed in a table format''')
    Questions = ['Select your Question',
        '1.What are the names of all the videos and their corresponding channels?',
        '2.Which channels have the most number of videos, and how many videos do they have?',
        '3.What are the top 10 most viewed videos and their respective channels?',
        '4.How many comments were made on each video, and what are their corresponding video names?',
        '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '7.What is the total number of views for each channel, and what are their corresponding channel names?',
        '8.What are the names of all the channels that have published videos in the year 2022?',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names?' ]
    
    Selected_Question = st.selectbox(' ',options=Questions)
    if Selected_Question =='1.What are the names of all the videos and their corresponding channels?':
        with st.spinner('Ploting in progress...'):
            Q1 = db_manager.sql_question_1()
            st.dataframe(Q1)
    if Selected_Question =='2.Which channels have the most number of videos, and how many videos do they have?':
        with st.spinner('Ploting in progress...'):
            Q2 = db_manager.sql_question_2()
            st.dataframe(Q2)
    if Selected_Question =='3.What are the top 10 most viewed videos and their respective channels?':
        with st.spinner('Ploting in progress...'): 
            Q3 =db_manager.sql_question_3()
            st.dataframe(Q3)
    if Selected_Question =='4.How many comments were made on each video, and what are their corresponding video names?':
        with st.spinner('Ploting in progress...'):
            Q4 = db_manager.sql_question_4()
            st.dataframe(Q4)  
    if Selected_Question =='5.Which videos have the highest number of likes, and what are their corresponding channel names?':
        with st.spinner('Ploting in progress...'):
            Q5 = db_manager.sql_question_5()
            st.dataframe(Q5) 
    if Selected_Question =='6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        st.write('**:red[Note]:- Dislike property was made private as of December 13, 2021.**')
        with st.spinner('Ploting in progress...'):
            Q6 = db_manager.sql_question_6()
            st.dataframe(Q6)   
    if Selected_Question =='7.What is the total number of views for each channel, and what are their corresponding channel names?':
        with st.spinner('Ploting in progress...'):
            Q7 = db_manager.sql_question_7()
            st.dataframe(Q7)
    if Selected_Question =='8.What are the names of all the channels that have published videos in the year 2022?':
        with st.spinner('Ploting in progress...'):
            Q8 = db_manager.sql_question_8()
            st.dataframe(Q8)
    if Selected_Question =='9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        with st.spinner('Ploting in progress...'):
            Q9 = db_manager.sql_question_9()
            st.dataframe(Q9)
    if Selected_Question =='10.Which videos have the highest number of comments, and what are their corresponding channel names?':
        with st.spinner('Ploting in progress...'):
            Q10 = db_manager.sql_question_10()
            st.dataframe(Q10)