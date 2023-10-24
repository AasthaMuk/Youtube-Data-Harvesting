# %% [markdown]
# # Importing Libraries

# %%
! pip install googleapiclient

# %%
import googleapiclient.discovery
import googleapiclient.errors
import pymongo
import psycopg2

# %%
import streamlit as st
import pandas as pd

st.write(1234)
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))

# %% [markdown]
# # Different APIs to do Data Scraping

# %% [markdown]
# ### Using Youtube API by Google using API Key

# %%
def access_youtube_api():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyCHQnJVCzO8z0sD2qcCKR0MCawdHvnACEo"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version,developerKey=api_key)
    return youtube

# %% [markdown]
# ### Saving in MongoDB data lake

# %%
client = pymongo.MongoClient("mongodb://localhost:27017")

document = client['youtube'] # database
channel_collection = document['Channel'] # table-1


# %%
def insert_channel(channel_info,video):
    x = channel_collection.insert_one({"Channel_Name":channel_info,"Videos":video})

# %% [markdown]
# ### Migrating Data from MongoDB to Postgresql

# %%
conn = psycopg2.connect(database="youtube_db",host="localhost",user="postgres",password="root",port="5432")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE Channel(channel_id VARCHAR(255),channel_name VARCHAR(255),
                channel_type VARCHAR(255),channel_views INT,channel_description TEXT,channel_status VARCHAR(255))''')
conn.commit()

print("Channel Table Created successfully")


# %%
def create_channel(row): 
    channel_id = row['Channel_Id']
    channel_name = row['Channel_Name']
    channel_views = row['Channel_Views']
    channel_description = row['Channel_Description']

    cursor.execute("""
     INSERT INTO Channel(channel_id,channel_name,channel_views,channel_description) VALUES(
          %s,%s,%s,%s)""",(channel_id,channel_name,channel_views,channel_description))
    conn.commit()
    

# %% [markdown]
# ### Channel,Video,Caption and Comment Details

# %% [markdown]
# Fetch the Channel Details using Channel_Id

# %%
def get_channel_details():
    youtube = access_youtube_api()
    channel_request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UCeVMnSShP_Iviwkknt83cww" # channel_id
    )
    
    channel_response = channel_request.execute()
    items = channel_response['items'][0]

    channel_id = items['id']
    channel_name = items['snippet']['title']
    channel_description = items['snippet']['description']
    subscription_count = items['statistics']['subscriberCount']
    channel_views = items['statistics']['viewCount']
    playlist_id = items['contentDetails']['relatedPlaylists']['uploads']

    channel_info = {"Channel_Name":channel_name,
        "Channel_Id":channel_id,
        "Subscription_Count": subscription_count,
        "Channel_Views": channel_views,
        "Channel_Description": channel_description,
        "Playlist_Id": playlist_id
    }
    return channel_info
    

# %% [markdown]
# - Fetch playlistitems using PlayList_Id
# - Fetch video details using Video_Id
# - Fetch Caption Details using Video_Id
# - Fetch Comment Details using Video_Id

# %%
def playlist_details(youtube,channel_info):
    playlist_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId=channel_info['Playlist_Id'] # playlist_id ( found from channel )
    )
    
    playlist_response = playlist_request.execute()
    # print(playlist_response)
    return playlist_response

# %%
def video_details(youtube,video_id):
    video_request = youtube.videos().list(
            part="snippet,contentDetails,status,statistics",
            id=video_id) # video_id ( found from playlist_items response)
        
    video_response = video_request.execute()
    # print(video_response)
    return video_response

# %%
def caption_details(youtube,video_id):
    caption_request = youtube.captions().list(
                 part="snippet",
                 videoId=video_id # video_id ( found from playlist_items response)
                 )
    caption_response = caption_request.execute()
    # print(caption_response)
    return caption_response

# %%
def comment_details(youtube,video_id):
    comment_request = youtube.commentThreads().list(
                 part="snippet,replies",
                 videoId=video_id # video_id ( found from playlist_items response)
            )
    comment_response = comment_request.execute()
    # print(comment_response)
    return comment_response

# %%
def videos_info(video_id,video_response,caption_response,comment_response):
    video_info = {
                "Video_Id": video_id,
                "Video_Name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                "Video_Description": video_response['items'][0]['snippet']['description'],
                "Tags": ["example", "video"],
                "PublishedAt": video_response['items'][0]['snippet']['publishedAt'],
                "View_Count": video_response['items'][0]['statistics']['viewCount'],
                "Like_Count": video_response['items'][0]['statistics']['likeCount'],
                "Dislike_Count": video_response['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in video_response['items'][0]['statistics'] else "Not Available",
                "Favorite_Count": video_response['items'][0]['statistics']['favoriteCount'],
                "Comment_Count": video_response['items'][0]['statistics']['commentCount'],
                "Duration": video_response['items'][0]['contentDetails']['duration'],
                "Thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url']
            }
            
    if caption_response['items']:
        caption_status = caption_response['items'][0]['snippet']['status']
        video_info["Caption_Status"] = caption_status
    else :
        video_info["Caption_Status"] = "Not Available"
    
    comments = dict()
    for comment in comment_response['items']:
        comment_details = {
            "Comment_Id":comment['snippet']['topLevelComment']['id'],
            "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
            "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']
        }
        comments[comment_details['Comment_Id']] = comment_details
        
    # print(video_info)
    video_info["Comments"] = comments
    
    return video_info

# %%
def get_videos_details():
    channel_info = get_channel_details()
    youtube = access_youtube_api()
    playlist_response = playlist_details(youtube,channel_info)
    playlistitems = playlist_response['items']

    video=dict()

    for item in playlistitems:
        video_id = item['contentDetails']['videoId']
        video_response = video_details(youtube,video_id)
        
        if video_response['items']:
            caption_response = caption_details(youtube,video_id)
            comment_response = comment_details(youtube,video_id)
            video_info = videos_info(video_id,video_response,caption_response,comment_response)
            video[video_id] = video_info
            
    return video
    

# %% [markdown]
# # Executing Main

# %%
channel_info = get_channel_details()
videos = get_videos_details()
insert_channel(channel_info=channel_info,video=videos)


# for row in channel_name_collection.find():
#     print(row)
#     create_channel(row)


# cursor.execute("SELECT * FROM channel") 
# conn.close()


