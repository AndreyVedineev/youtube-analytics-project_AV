import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
api_key = os.getenv('YT_API_KEY')


# class HttpError(Exception):
#     """Класс исключения несуществующий id видео"""
#
#     def __init__(self, message, base_message=None):
#         self.base_message = base_message
#         self.message = message
#
#     def __str__(self):
#         if self.base_message is None:
#             return self.message
#
#         return f'{self.message} - {str(self.base_message)}'


class Video:
    """
    Работа с видеороликом из youtube
    """

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.url = f"https://youtu.be/{self.video_id}"

        if not self.constructor()['items']:
            self.title = None
            self.url = None
            self.count_video = None
            self.count_like = None
        else:
            self.title = self.constructor()['items'][0]['snippet']['title']  # название видео
            self.url = f"https://youtu.be/{self.video_id}"  # ссылка на видео
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
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            video = youtube.captions().list(videoId=self.video_id, part='snippet').execute()

        except HttpError:
            print("_несуществующий id видео_")

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
