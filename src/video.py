import json
import os

from dotenv import load_dotenv
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YT_API_KEY')
channel_id = 'UCjWOzgG0oTFHy4N4BeDmBhg'


class Video:
    """

    """

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.channel_id = channel_id
        # self.id_video = id_video  # id видео
        # self.title = title  # название видео
        # self.url = url  # ссылка на видео
        # self.count_video = count_video  # количество просмотров
        # self.count_like = count_like  # количество лайков

    def constructor(self):
        """
        Возвращает инфо по video
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists = youtube.playlists().list(channelId=self.channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()


        return playlists


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


video1 = Video('9lO06Zxhu88')  # '9lO06Zxhu88' - это id видео из ютуб

# print(json.dumps(video1.constructor(), indent=2, ensure_ascii=False))
for playlist in video1.constructor()['items']:
    print(playlist)
    print()