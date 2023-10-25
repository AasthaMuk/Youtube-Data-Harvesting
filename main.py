import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

with header:
    st.title("Welcome to my Data Science Project")
    st.text("Looking into transaction for taxis in NYC")

with dataset:
    st.title("NYC taxi dataset")

with features:
    st.title("Features created")

with model_training:
    st.title("Time to train the model")

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

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )