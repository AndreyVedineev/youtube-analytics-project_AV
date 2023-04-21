import json
import os

from dotenv import load_dotenv
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""

        self.__channel_id = channel_id  # id канала
        self.title = self.constructor()['items'][0]['snippet']['title']  # название канала
        self.video_count = self.constructor()['items'][0]['statistics']['videoCount']  # количество видео
        self.description = self.constructor()['items'][0]['snippet']['description']  # описание канала
        self.url = self.constructor()['items'][0]['snippet']['thumbnails']['high']['url']
        self.view_count = self.constructor()['items'][0]['statistics']['viewCount']  # количество подписчиков

        # self.viewCount = viewCount  # общее количество просмотров

    @staticmethod
    def get_service():
        """ Ресурсный объект для взаимодействия с API youtube"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def constructor(self):
        """Возвращает инфо по каналу"""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    def to_json(self, file):
        """Cохраняет в файл значения атрибутов экземпляра Channel"""
        data = {'channel_id': self.__channel_id,
                'title': self.title,
                'video_count': self.video_count,
                'description': self.description.replace("\n", ""),
                'url': self.url,
                'view_count': self.view_count
                }

        with open(file, 'w', encoding='UTF-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
