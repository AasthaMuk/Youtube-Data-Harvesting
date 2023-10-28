import streamlit as st
import pandas as pd

class Queries:

    def __init__(self):
        pass

    def query1(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                          inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')


    def query2(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')


    def query3(self,cursor):
        cursor.execute("""SELECT v.video_name,v.view_count,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join Channel c
                          on c.channel_name = p.channel_name order by v.view_count desc limit 10""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','view_count','channel_name'])
        st.table(data)
        # st.bar_chart(data,x='video_name',y='channel_name')


    def query4(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query5(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query6(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query7(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query8(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query9(self,cursor):
        cursor.execute("""SELECT v.video_name,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id 
                                inner join Channel c on c.channel_name=p.channel_name""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','channel_name'])
        st.table(data)
        st.bar_chart(data,x='video_name',y='channel_name')

    def query10(self,cursor):
        cursor.execute("""SELECT v.video_name,v.comment_count,c.channel_name from Video v inner join Playlist p on v.playlist_id = p.playlist_id inner join Channel c
                          on c.channel_name=p.channel_name where v.comment_count = ( SELECT MAX(comment_count) from Video)""")
        data = pd.DataFrame(cursor.fetchall(),columns=['video_name','comment_count','channel_name'])
        st.table(data)
        # st.bar_chart(data,x='video_name',y='channel_name')