import streamlit as st
import pandas as pd
from api import *


if __name__=="__main__":
    app = Utilities()
    channel_info = app.get_channel_details()
    videos = app.get_videos_details()
    app.insert_channel(channel_info,videos)

    header = st.container()
    with header:
        st.title("Welcome to my Data Science Project")
        st.text("Looking into transaction for taxis in NYC")
        st.text(channel_info)


    add_selectbox = st.sidebar.selectbox(
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





