import streamlit as st
import pymongo
import psycopg2
from api import *
from queries import *
from psycopg2.errors import *


def insert_channel(channel_id):
    channel = createMongoDBLake()
    app = Utilities()
    
    cursor = channel.find({"Channel_Name.Channel_Id": channel_id})
    
    if len(list(cursor)) == 0:
        with st.spinner("Saving into MongoDB ....."):
            channel_info = app.get_channel_details(channel_id)
            video = app.get_videos_details(channel_id)
            channel.insert_one({"Channel_Name":channel_info,"Videos":video})
        st.write(":smile: Data Got Saved to MongoDB :smile:")
    else:
        st.toast('🔥 Please Enter Unique Record, the data is already present in Data Lake !!')



def createMongoDBLake():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    document = client['youtube'] # database
    channel_collection = document['Channel'] # table-1
    return channel_collection
    
    


def getChannelCollectionData(channel_name):
    channel_collection = createMongoDBLake()
    channel_details = dict()
    video_details =  dict()
    for row in channel.find({"Channel_Name.Channel_Name": channel_name}):
        channel_details = row['Channel_Name']
        video_details = row['Videos']

    return channel_details,video_details



def createSQLTables():
    conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Channel(channel_id VARCHAR(255) PRIMARY KEY,channel_name VARCHAR(255),
                channel_views INT,subscription_count INT,channel_description TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Playlist(playlist_id VARCHAR(255) PRIMARY KEY,channel_name VARCHAR(255))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Comment(comment_id VARCHAR(255) PRIMARY KEY,video_id VARCHAR(255),
                comment_text TEXT,comment_author VARCHAR(255),comment_published_date TIMESTAMP)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Video(video_id VARCHAR(255) PRIMARY KEY,playlist_id VARCHAR(255),
                video_name VARCHAR(255),video_description TEXT,published_date TIMESTAMP,view_count INT,like_Count INT,
                dislike_count INT,favourite_count INT,comment_count INT,duration INT,thumbnail VARCHAR(255),
                caption_status VARCHAR(255))''')
    conn.commit()
    conn.close()
    
    
def convertIntoSeconds(time):
      h,m,s = time.split(":")
      sec = int(h)*3600 + int(m)*60 + int(s)
      return sec




def insert_Data_SQL(ch_name): 
    conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    channel , video = getChannelCollectionData(ch_name)
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
        dislike_count = int(video[i]['Dislike_Count'])
        favourite_count = video[i]['Favorite_Count']
        comment_count = video[i]['Comment_Count']
        duration = convertIntoSeconds(video[i]['Duration'])
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
    conn.close()
    print("Tables Created successfully")
    
    

def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


def select_SQL_query():
    option = st.sidebar.selectbox(
        "Enter any queries you like :",
        ("--Select--",
         "What are the names of all the videos and their corresponding channels?",
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
    return option


def execute_Query(select_query):
    q = Queries()
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




if __name__=="__main__":
    
    conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
    cursor = conn.cursor()
    
    
    header = st.container()
    with header:
        st.title("Project : YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit")
        st.text("This project aims to develop a user-friendly Streamlit application that utilizes ")
        st.text("the Google API to extract information on a YouTube channel, stores it in a ")
        st.text("MongoDB database, migrates it to a SQL data warehouse, and enables users to search ")
        st.text("for channel details and join tables to view data in the Streamlit app.")

        if "my_text" not in st.session_state:
              st.session_state.my_text = ""

        st.text_input("Enter Channel Id :",key='widget', on_change=clear_text)
        # channel_id = st.text_input("Enter Channel Id :")
        channel_id = st.session_state.my_text
        # st.write(channel_id)
        # print(channel_id)

        channel = createMongoDBLake()
        
        channel_name =""
        channel_names=["--Select--"]

        print(channel.count_documents({}))
        if channel.count_documents({}) < 10:
            result = st.button("Save to Mongo Data Lake", type="primary")
            if result:
                if channel_id:
                   insert_channel(channel_id)
                   del st.session_state['my_text']
        else:        
            st.write("Data is full !! 10 Records in place")

        
        

        for row in channel.find():
            channel_names.append(row['Channel_Name']['Channel_Name'])
        

        selected_channel = st.selectbox(
            "Select a channel",
            options = channel_names,
        )

        flag = st.button("Migrate to SQL", type="primary")
        if flag:
            try:
                createSQLTables()
                insert_Data_SQL(selected_channel)
                st.success("Data saved to SQL!!")
            except UniqueViolation as e:
                 st.toast("🔥 Data already present in DB, Please check !!!")
            
        select_query = select_SQL_query()
        execute_Query(select_query)

        # if channel_id :
        #       createSQLTables()
        #       insert_Data_SQL(channel_id)
            #   try:
            #         insert_Data_SQL(channel_id)
            #   except:
            #         # st.error('Please Enter Unique Data, it seems that the data is already present in the Database !!', icon="🚨")
            #         st.toast('Please Enter Unique Data, it seems that the data is already present in the Database', icon="🔥")
            #         del st.session_state['my_text']


        
        




    

    






