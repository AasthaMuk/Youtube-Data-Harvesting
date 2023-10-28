import streamlit as st
import pymongo
import psycopg2
from api import *
from queries import *

@st.cache_resource
def insert_channel(_channel,channel_info,video):
    x = _channel.insert_one({"Channel_Name":channel_info,"Videos":video})


@st.cache_resource
def createMongoDBLake(channel_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    document = client['youtube'] # database
    channel_collection = document['Channel'] # table-1
    app = Utilities()
    channel_info = app.get_channel_details(channel_id)
    videos = app.get_videos_details(channel_id)    
    insert_channel(channel_collection,channel_info,videos)
    return channel_collection

@st.cache_resource
def getChannelCollectionData(channel_id):
    channel = createMongoDBLake(channel_id)
    channel_details = dict()
    video_details =  dict()
    for row in channel.find():
        channel_details = row['Channel_Name']
        video_details = row['Videos']
        print(type(channel_details))

    return channel_details,video_details

@st.cache_resource
def createSQLTables():
    conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE Channel(channel_id VARCHAR(255),channel_name VARCHAR(255),
                channel_views INT,subscription_count INT,channel_description TEXT)''')
    
    cursor.execute('''CREATE TABLE Playlist(playlist_id VARCHAR(255),channel_name VARCHAR(255))''')
    
    cursor.execute('''CREATE TABLE Comment(comment_id VARCHAR(255),video_id VARCHAR(255),
                comment_text TEXT,comment_author VARCHAR(255),comment_published_date TIMESTAMP)''')
    
    cursor.execute('''CREATE TABLE Video(video_id VARCHAR(255),playlist_id VARCHAR(255),
                video_name VARCHAR(255),video_description TEXT,published_date TIMESTAMP,view_count INT,like_Count INT,
                dislike_count VARCHAR(255),favourite_count INT,comment_count INT,duration VARCHAR(255),thumbnail VARCHAR(255),
                caption_status VARCHAR(255))''')
    conn.commit()
    return conn,cursor


@st.cache_resource
def insert_Data_SQL(channel_id): 
    conn,cursor = createSQLTables()
    channel , video = getChannelCollectionData(channel_id)
    channel_id = channel['Channel_Id']
    channel_name = channel['Channel_Name']
    subscription_count = int(channel['Subscription_Count'])
    channel_views = int(channel['Channel_Views'])
    channel_description = channel['Channel_Description']

    for i in video:
        video_id = video[i]['Video_Id']
        playlist_id = channel['Playlist_Id']
        video_name = video[i]['Video_Name']
        video_description = video[i]['Video_Description']
        published_date = video[i]['PublishedAt']
        view_count = int(video[i]['View_Count'])
        like_Count = int(video[i]['Like_Count'])
        dislike_count = video[i]['Dislike_Count']
        favourite_count = video[i]['Favorite_Count']
        comment_count = video[i]['Comment_Count']
        duration = video[i]['Duration']
        thumbnail = video[i]['Thumbnail']
        caption_status = video[i]['Caption_Status']

        cursor.execute("""
          INSERT INTO Video(video_id,playlist_id,video_name,video_description,published_date,view_count,like_Count,
          dislike_count,favourite_count,comment_count,duration,thumbnail,caption_status) VALUES(
          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(video_id,playlist_id,video_name,video_description,published_date,view_count,like_Count,
          dislike_count,favourite_count,comment_count,duration,thumbnail,caption_status))
        
        comments = video[i]['Comments']
        for comment in comments:
            comment_id = comments[comment]['Comment_Id']
            comment_text = comments[comment]['Comment_Text']
            comment_author = comments[comment]['Comment_Author']
            comment_published_date = comments[comment]['Comment_PublishedAt']

            cursor.execute("""
              INSERT INTO Comment(comment_id,video_id,comment_text,comment_author,comment_published_date) 
              VALUES(%s,%s,%s,%s,%s)""",(comment_id,video_id,comment_text,comment_author,
              comment_published_date))
            

    cursor.execute("""
     INSERT INTO Channel(channel_id,channel_name,channel_views,subscription_count,channel_description) VALUES(
          %s,%s,%s,%s,%s)""",(channel_id,channel_name,channel_views,subscription_count,channel_description))
    
    cursor.execute("""
          INSERT INTO Playlist(playlist_id,channel_name) VALUES(%s,%s)""",(playlist_id,channel_name))
    
    conn.commit()
    print("Tables Created successfully")
    conn.close()




if __name__=="__main__":
    
    
    conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    
    q = Queries()

    header = st.container()

    select_query = st.sidebar.selectbox(
        "Enter any queries you like :",
        ("What are the names of all the videos and their corresponding channels?",
         "Which channels have the most number of videos, and how many videos do they have?",
         "What are the top 10 most viewed videos and their respective channels?",
         "How many comments were made on each video, and what are their corresponding video names?",
         "Which videos have the highest number of likes, and what are their corresponding channel names?",
         "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
         "What is the total number of views for each channel, and what are their corresponding channel names?",
         "What are the names of all the channels that have published videos in the year 2022?",
         "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
         "Which videos have the highest number of comments, and what are their corresponding channel names?"
        )
    )

    with header:
        st.title("Project : YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit")
        st.text("This project aims to develop a user-friendly Streamlit application that utilizes ")
        st.text("the Google API to extract information on a YouTube channel, stores it in a MongoDB database,")
        st.text("migrates it to a SQL data warehouse, and enables users to search for channel details and")
        st.text("join tables to view data in the Streamlit app.")

        channel_id = st.text_input("Enter Channel Id :")
        if channel_id :
            # insert_Data_SQL(channel_id)

            if "What are the names of all the videos and their corresponding channels?" in select_query:
                q.query1(cursor)
            elif "Which channels have the most number of videos, and how many videos do they have?" in select_query:
                q.query2(cursor)
            elif "What are the top 10 most viewed videos and their respective channels?" in select_query:
                q.query3(cursor)
            elif "How many comments were made on each video, and what are their corresponding video names?" in select_query:
                q.query4(cursor)
            elif "Which videos have the highest number of likes, and what are their corresponding channel names?" in select_query:
                q.query5(cursor)
            elif "What is the total number of likes and dislikes for each video, and what are their corresponding video names?" in select_query:
                q.query6(cursor)
            elif "What is the total number of views for each channel, and what are their corresponding channel names?" in select_query:
                q.query7(cursor)
            elif "What are the names of all the channels that have published videos in the year 2022?" in select_query:
                q.query8(cursor)
            elif "What is the average duration of all videos in each channel, and what are their corresponding channel names?" in select_query:
                q.query9(cursor)
            elif "Which videos have the highest number of comments, and what are their corresponding channel names?" in select_query:
                q.query10(cursor)




    

    






