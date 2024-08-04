import streamlit as st
from PIL import Image

# Main Title
st.title(':red[YouTube Data Harvesting & Warehousing using MySQL]')

# Subtitle
st.header(':blue[A project by Mohammed Jeseem]')

# Using columns to organize layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(':blue[Domain:] Social Media')
    st.subheader(':blue[Overview:]')
    st.write('''Build a simple dashboard or UI using Streamlit and 
                retrieve YouTube channel data with the help of the YouTube API.
                Store the data in an MySQL database (warehousing) managed by the MySQL workbench,
                enabling querying of the data using SQL. Visualize the data within the Streamlit app to uncover insights,
                and trends with the YouTube channel data.''')

    st.subheader(':blue[Skill Take Away:]')
    st.write('Python scripting, Data Collection, API integration, Data Management using MySQL, Streamlit')

    st.subheader(':blue[About:]')
    st.write('''Hi! I'm Mohammed Jeseem, a mobile app developer with 6 years of experience and a Computer Science degree. 
                Currently, I'm delving into data science and analytics. My first project, 
                "YouTube Data Harvesting and Warehousing using MySQL," 
                explores extracting insights from YouTube data. 
                This journey has fueled my passion for data-driven decision-making and sharpened my skills in data extraction, 
                analysis, and database management.''')

with col2:
    icon = Image.open("images/youtube.png")
    st.image(icon, caption='YouTube Data Harvesting Project', use_column_width=True)

# Contact Information
st.subheader(':blue[Contact:]')
st.write(':blue[LinkedIn:] [Mohammed Jeseem](https://www.linkedin.com/in/mohammed-jeseem-25894b29b/)')
st.write(':blue[Email:] mohammedjezeem786@gmail.com')




            



