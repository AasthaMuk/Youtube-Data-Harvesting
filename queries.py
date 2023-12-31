import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Class created to have all the queries in one place
class Queries:

    def __init__(self):
        pass

    def query1(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                          inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)

        data = data.iloc[9:34,:]
        x_values = data['video_name']
        y_values = data['channel_name']
        fig, ax = plt.subplots()
        ax.scatter(x_values, y_values)

        # Add labels and title
        ax.set_xlabel("video names")
        ax.set_ylabel("channel names")
        ax.set_title("Scatter Plot for Video Names")

        st.pyplot(fig)
        


    def query2(self,cursor):
        cursor.execute("""WITH CTE AS(
        SELECT c.channel_name,count(v.video_name) as count_of_videos from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join Channel c
        on c.channel_name = p.channel_name where v.duration>400 group by c.channel_name
        )
        SELECT  c.channel_name,c.count_of_videos as max_no_of_videos from CTE c 
        where c.count_of_videos=(SELECT MAX(c1.count_of_videos) FROM CTE c1)""")

        data = pd.DataFrame(cursor.fetchall(),columns=['channel_name','max_no_of_videos'])
        st.table(data)
        st.bar_chart(data,x='channel_name',y='max_no_of_videos')


    def query3(self,cursor):
        cursor.execute("""SELECT v.video_name,v.view_count,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join Channel c
                          on c.channel_name = p.channel_name order by v.view_count desc limit 10""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','view_count','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='view_count')


    def query4(self,cursor):
        cursor.execute("""SELECT count(c.comment_id) as No_of_comments,v.video_name from Comment c inner join 
                            Video v on c.video_id=v.video_id group by v.video_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['No_of_comments','video_name'])
        st.table(data.head(10))
        st.bar_chart(data.head(20),x='video_name',y='No_of_comments')


    def query5(self,cursor):
        cursor.execute("""SELECT v.like_count as Max_Likes,v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join 
                       Channel c on c.channel_name = p.channel_name WHERE v.like_count = 
                       (SELECT MAX(like_count) from Video)""")
        data = pd.DataFrame(cursor.fetchall(),columns=['Max_Likes','video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='Max_Likes')


    def query6(self,cursor):
        cursor.execute("""SELECT like_count,dislike_count,video_name from Video""")
        data = pd.DataFrame(cursor.fetchall(),columns=['like_count','dislike_count','video_name'])
        st.table(data.head(9))
        st.bar_chart(data.head(9),x='video_name',y='like_count')


    def query7(self,cursor):
        cursor.execute("""SELECT channel_name, channel_views FROM Channel""")
        data = pd.DataFrame(cursor.fetchall(),columns=['channel_name', 'channel_views'])
        st.table(data)
        st.line_chart(data,x='channel_name',y='channel_views')


    def query8(self,cursor):
        cursor.execute("""SELECT v.video_name,v.published_date,c.channel_name FROM Video v inner join Playlist p on v.playlist_id =
                       p.playlist_id inner join Channel c on c.channel_name = p.channel_name where 
                       EXTRACT(YEAR FROM v.published_date)='2023'""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','published_date','channel_name'])
        st.table(data.iloc[9:34,:])
        st.line_chart(data.iloc[9:34,:],x='published_date',y='video_name')


    def query9(self,cursor):
        cursor.execute("""SELECT c.channel_name,ROUND(AVG(v.duration),1) as average_duration from Video v INNER JOIN Playlist p ON
                        v.playlist_id = p.playlist_id INNER JOIN Channel c ON c.channel_name = p.channel_name
                        group by c.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['channel_name','average_duration'])
        st.table(data)
        
        
        y_values = np.round(data['average_duration'].apply(float),0)
        x_values = data['channel_name']
        plt.figure(figsize=(7, 6))
        bars = plt.bar(x_values, y_values)

        for bar, label in zip(bars, data['channel_name']):
            plt.text(bar.get_x() + bar.get_width(), bar.get_height(), label, ha='center')

        plt.xticks([])
        plt.xlabel("Channel Name")
        plt.ylabel("Average Duration")
        plt.title("Average Duration by Channel")
        st.pyplot(plt)




    def query10(self,cursor):
        cursor.execute("""SELECT v.video_name,v.comment_count,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join Channel c
                          on c.channel_name=p.channel_name where v.comment_count = ( SELECT MAX(comment_count) from Video)""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','comment_count','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='comment_count')