import json
import os

from dotenv import load_dotenv
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv('YT_API_KEY')


def get_service():
    """ Ресурсный объект для взаимодействия с API youtube"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
