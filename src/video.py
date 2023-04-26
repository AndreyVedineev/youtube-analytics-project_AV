import json
import os

from dotenv import load_dotenv
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YT_API_KEY')


class Video:
    """

    """

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = self.constructor()['items'][0]['snippet']['title']  # название видео
        # self.url = self.constructor()['items'][0]['snippet']['thumbnails']['high']['url']  # ссылка нe на видео!!!!
        # self.count_video = self.constructor()['items'][0]['statistics']['viewCount']  # количество просмотров
        # self.count_like = self.constructor()['items'][0]['statistics']['likeCount']  # количество лайков

    def constructor(self):
        """
        Возвращает инфо по video
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=self.video_id
                                          ).execute()

        return playlists

    # def __str__(self):
    #     return self.title


class PLVideo:
    """Создайте второй класс для видео `PLVideo`, который инициализируется  'id видео' и 'id плейлиста'
> Видео может находиться в множестве плейлистов, поэтому непосредственно из видео через API информацию о плейлисте не получить.
- Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `PLVideo`:
  - id видео
  - название видео
  - ссылка на видео
  - количество просмотров
  - количество лайков
  - id плейлиста

    """

    def __init__(self):
        pass


video1 = Video('9lO06Zxhu88')

print(json.dumps(video1.constructor()))
