import streamlit as st
import plotly.express as px
from src.mysql_db.mysql_db_request import database_manager_instance

# Initialize MySQL singleton class instances
db_manager = database_manager_instance

if True:
    st.subheader(':blue[Data Visualization]')
    st.markdown('''you can view statistical analyses of YouTube channels along with visualizations''')

    Option = st.selectbox(' ',['Select to view ',
                        '1.Channels with subscriber count',
                        '2.Channels with highest no of videos',
                        '3.Channels with top 10 viewed videos',
                        '4.Channels with total views',
                        '5.channels with average videos duration',
                        '6.Year wise performance of each channel'])
    
    if Option =='1.Channels with subscriber count':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_channels_subscribers()
            fig=px.bar(df, x='Channel Name', y='Subscribers Count',color='Channel Name',text='Subscribers Count',
                         title='Channels with Subscriber Count')
            st.plotly_chart(fig, use_container_width=True)
    
    if Option == '2.Channels with highest no of videos':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_channels_videos()
            fig =px.bar(df, x='Channel Name', y='Total Videos',color='Channel Name',text='Total Videos',
                        title='Channels with highest No Of Videos')
            st.plotly_chart(fig,use_container_width=True) 
        
    if Option =='3.Channels with top 10 viewed videos':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_top_10_viewed_videos()
            fig=px.bar(df, x='Total Views', y='Video Name', color='Channel Name',text='Total Views',
                        orientation='h', title='Top 10 Viewed Videos for Each Channel')
            st.plotly_chart(fig,use_container_width=True) 
        
    if Option =='4.Channels with total views':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_channels_total_views()
            fig=px.bar(df, x='Total Views', y='Channel Name', color='Channel Name',text='Total Views',
                        title='Channels with Total Views')
            st.plotly_chart(fig,use_container_width=True) 

    if Option =='5.channels with average videos duration':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_channels_average_duration()
            fig=px.bar(df, x='Channel Name', y='Average Duration', color='Channel Name',text='Average Duration',
                        title='Channels with Average Duration')
            st.plotly_chart(fig,use_container_width=True)

    if Option =='6.Year wise performance of each channel':
        with st.spinner('Ploting in progress...'):
            df=database_manager_instance.plot_yearwise_performance()
            fig=px.line(df, x='Years', y='Total Videos', color='Channel Name',markers=True,
                        title='Year wise uploaded videos')
            st.plotly_chart(fig)

            fig1=px.line(df, x='Years', y='Likes', color='Channel Name',markers=True,
                        title='Year wise Likes')
            st.plotly_chart(fig1)

            fig2=px.line(df, x='Years', y='Views', color='Channel Name',markers=True,
                        title='Year wise Views')
            st.plotly_chart(fig2)

            fig3=px.line(df, x='Years', y='Total Comments', color='Channel Name',markers=True,
                        title='Year wise Comments')
            st.plotly_chart(fig3)
        
        
        
        
            