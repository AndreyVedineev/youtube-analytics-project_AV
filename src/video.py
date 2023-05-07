import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YT_API_KEY')


class Video:
    """
    Работа с видеороликом из youtube
    """

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = self.constructor()['items'][0]['snippet']['title']  # название видео
        self.url = self.constructor()['items'][0]['snippet']['thumbnails']['high']['url']  # ссылка нe на видео!!!!
        self.count_video = self.constructor()['items'][0]['statistics']['viewCount']  # количество просмотров
        self.count_like = self.constructor()['items'][0]['statistics']['likeCount']  # количество лайков

    def constructor(self):
        """
        Возвращает инфо по video
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=self.video_id
                                          ).execute()

        return playlists

    def __str__(self):
        return self.title

    def count_video(self):
        return self.count_video()


class PLVideo(Video):
    """
    Информация о видео в плейлисте
    """

    def __init__(self, video_id, playlist_id):


        self.video_id = video_id  # id видео
        self.playlist_id = playlist_id  # id плейлиста
        self.title = self.find_id_video()  # название видео
        self.url = self.constructor()['items'][0]['snippet']['thumbnails']['high']['url']  # ссылка нe на видео!!!!

    def constructor(self):
        """
        Возвращает инфо по playlists
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='snippet, contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        return playlist_videos

    def find_id_video(self):
        for part_pl in range(len(self.constructor())):
            if self.constructor()['items'][part_pl]['contentDetails']['videoId'] == self.video_id:
                return self.constructor()['items'][part_pl]['snippet']['title']
            else:
                continue

    def __str__(self):
        return self.title

    def count_video(self):
        """
        Количество просмотров
        """
        video = Video(self.video_id)
        return video.constructor()['items'][0]['statistics']['viewCount']

    def count_like(self):
        """
        Количество лайков
        """
        video = Video(self.video_id)
        return video.constructor()['items'][0]['statistics']['likeCount']
