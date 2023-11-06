import googleapiclient.discovery
import googleapiclient.errors


# Class created to have all the utility methods in one place
class Utilities:

    def __init__(self):
        pass
    
    # ------------------------  Different Methods created ---------------------------------#
    def access_youtube_api(self):
        api_service_name = "youtube"
        api_version = "v3"
        api_key = "AIzaSyCh0dd26vYWV2XnUV1mJcfnXATorQw1WLQ"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version,developerKey=api_key)
        return youtube
    

    
    def get_channel_details(self,channel_id):
        youtube = self.access_youtube_api()
        channel_request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id = channel_id # channel_id
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
    


    def playlist_details(self,channel_id):
        youtube = self.access_youtube_api()
        channel_info = self.get_channel_details(channel_id)
        next_page_token = None
        list_of_video_ids = []
        no_of_pages = 1
        while True:
            playlist_request = youtube.playlistItems().list(
                part="snippet",
                playlistId=channel_info['Playlist_Id'], # playlist_id ( found from channel )
                maxResults=5,
                pageToken=next_page_token
            )

            playlist_response = playlist_request.execute()

            for playlistitem in playlist_response['items']:
                list_of_video_ids.append(playlistitem['snippet']['resourceId']['videoId'])

            next_page_token = playlist_response.get('nextPageToken')
            no_of_pages +=1
    
            if no_of_pages == 3:
                break

        return list_of_video_ids
        
    


    def get_videos_details(self,channel_id):
        video_ids_list = self.playlist_details(channel_id)
        video=dict()

        count = 1
        for item in video_ids_list:
                video_id = item
                video_response = self.video_details(video_id)
                
                if video_response['items']:
                    caption_response = self.caption_details(video_id)
                    comment_response = self.comment_details(video_id)
                    video_info = self.videos_info(video_id,video_response,caption_response,comment_response)
                    video['Video_Id_'+str(count)] = video_info

                count+=1

        return video
        
    


    def video_details(self,video_id):
        youtube = self.access_youtube_api()
        video_request = youtube.videos().list(
                part="snippet,contentDetails,status,statistics",
                id=video_id) # video_id ( found from playlist_items response)
            
        video_response = video_request.execute()
        return video_response
    

    def caption_details(self,video_id):
        youtube = self.access_youtube_api()
        caption_request = youtube.captions().list(
                    part="snippet",
                    videoId=video_id # video_id ( found from playlist_items response)
                    )
        caption_response = caption_request.execute()
        return caption_response
    



    def comment_details(self,video_id):
        youtube = self.access_youtube_api()

        list_of_comments = []
        next_page_token = None
        no_of_pages = 1
        while True :
            comment_request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id, # video_id ( found from playlist_items response)
                        maxResults=2,
                        pageToken=next_page_token
                    )
            comment_response = comment_request.execute()

            
            for c in comment_response.get('items',[]):
                snippet = c.get('snippet', {})
                topLevelComment = snippet.get('topLevelComment', {})
                is_comments_disabled = topLevelComment.get('snippet', {}).get('isPublic', True) is False
                if is_comments_disabled:
                    print(f"Comments are disabled for a comment thread on video with ID {video_id}. Skipping processing.")
                else:
                    # Process the comment thread as comments are enabled
                    print(f"Comments are enabled for a comment thread on video with ID {video_id}. Proceed with processing.")
                    list_of_comments.append(c)
                
            
            next_page_token = comment_response.get('nextPageToken')
            no_of_pages+=1

            if no_of_pages==2:
                break

        return list_of_comments
        
    



    def setDuration(self,time):
        s=""
        if "H" in time:
            time1 = time.split("H")[1]
            print(time1)
            h=time.split("H")[0]
            print(h)
            if int(h)<=9:
                s+="0"+h+":"
            else:
                s+=h+":"
        
            if "M" in time1:
                time2 = time1.split("M")[1]
                print(time2)
                m = time1.split("M")[0]
                print(m)
                if int(m)<=9:
                    s+="0"+m+":"
                else:
                    s+=m+":"

                if "S" in time1.split("M")[1]:
                    sec = time1.split("M")[1].split("S")[0]
                    print(sec)
                    if int(sec)<=9:
                        s+="0"+sec
                    else:
                        s+=sec
                else:
                    s+="00"
            else:
                s+="00"+":"
                if "S" in time1:
                    time3 = time1.split("S")[0]
                    if int(time3)<=9:
                        s+="0"+time3
                    else:
                        s+=time3
                else:
                    s+="00"
        else:
            if "M" in time:
                time1 = time.split("M")[1]
                print(time1)
                m = time.split("M")[0]
                print(m)
                s+="00"+":"
                if int(m)<=9:
                    s+="0"+m+":"
                else:
                    s+=m+":"
                
                if "S" in time.split("M")[1]:
                    sec = time.split("M")[1].split("S")[0]
                    print(sec)
                    if int(sec)<=9:
                        s+="0"+sec
                    else:
                        s+=sec
                else:
                    s+="00"
            else:
                if "S" in time:
                    time1 = time.split("S")[0]
                    s+="00:00"+":"
                    if int(time1)<=9:
                        s+="0"+time1
                    else:
                        s+=time1

        return s

    def videos_info(self,video_id,video_response,caption_response,comment_response):
        duration = video_response['items'][0]['contentDetails']['duration']
        time = duration.split("PT")[1]
        d = self.setDuration(time)
        
        video_info = {
                    "Video_Id": video_id,
                    "Video_Name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                    "Video_Description": video_response['items'][0]['snippet']['description'],
                    "Tags": video_response['items'][0]['snippet']['tags'],
                    "PublishedAt": video_response['items'][0]['snippet']['publishedAt'],
                    "View_Count": video_response['items'][0]['statistics']['viewCount'],
                    "Like_Count": video_response['items'][0]['statistics']['likeCount'] if 'likeCount' in video_response['items'][0]['statistics'] else 0,
                    "Dislike_Count": video_response['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in video_response['items'][0]['statistics'] else 0,
                    "Favorite_Count": video_response['items'][0]['statistics']['favoriteCount'] if 'favoriteCount' in video_response['items'][0]['statistics'] else 0,
                    "Comment_Count": video_response['items'][0]['statistics']['commentCount'] if 'commentCount' in video_response['items'][0]['statistics'] else 0,
                    "Duration": d,
                    "Thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url']
                }
                
        if caption_response['items']:
            caption_status = caption_response['items'][0]['snippet']['status']
            video_info["Caption_Status"] = caption_status
        else :
            video_info["Caption_Status"] = "Not Available"
        
        comments = dict()
        count=1
        for comment in comment_response:
            comment_details = {
                    "Comment_Id":comment['snippet']['topLevelComment']['id'],
                    "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']
                }
            comments['Comment_Id_'+str(count)] = comment_details
            count+=1
            
        video_info["Comments"] = comments
        
        return video_info
    
    #--------------------------------------------------------------------------------------#