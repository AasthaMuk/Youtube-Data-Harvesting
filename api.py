
import googleapiclient.discovery
import googleapiclient.errors

class Utilities:

    def __init__(self):
        pass

    def access_youtube_api(self):
        api_service_name = "youtube"
        api_version = "v3"
        api_key = "AIzaSyCHQnJVCzO8z0sD2qcCKR0MCawdHvnACEo"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version,developerKey=api_key)
        return youtube
    

    
    def get_channel_details(self):
        youtube = self.access_youtube_api()
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
    


    def playlist_details(self):
        youtube = self.access_youtube_api()
        channel_info = self.get_channel_details()
        playlist_request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId=channel_info['Playlist_Id'] # playlist_id ( found from channel )
        )
        playlist_response = playlist_request.execute()
        # print(playlist_response)
        return playlist_response
    


    def get_videos_details(self):
        channel_info = self.get_channel_details()
        youtube = self.access_youtube_api()
        playlist_response = self.playlist_details()
        playlistitems = playlist_response['items']

        video=dict()

        for item in playlistitems:
            video_id = item['contentDetails']['videoId']
            video_response = self.video_details(video_id)
            
            if video_response['items']:
                caption_response = self.caption_details(video_id)
                comment_response = self.comment_details(video_id)
                video_info = self.videos_info(video_id,video_response,caption_response,comment_response)
                video[video_id] = video_info
                
        return video
    


    def video_details(self,video_id):
        youtube = self.access_youtube_api()
        channel_info = self.get_channel_details()
        video_request = youtube.videos().list(
                part="snippet,contentDetails,status,statistics",
                id=video_id) # video_id ( found from playlist_items response)
            
        video_response = video_request.execute()
        # print(video_response)
        return video_response
    

    def caption_details(self,video_id):
        youtube = self.access_youtube_api()
        caption_request = youtube.captions().list(
                    part="snippet",
                    videoId=video_id # video_id ( found from playlist_items response)
                    )
        caption_response = caption_request.execute()
        # print(caption_response)
        return caption_response
    

    def comment_details(self,video_id):
        youtube = self.access_youtube_api()
        comment_request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id # video_id ( found from playlist_items response)
                )
        comment_response = comment_request.execute()
        # print(comment_response)
        return comment_response
    

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