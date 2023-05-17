import datetime
import os

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

from src.video import Video

load_dotenv()
api_key = os.getenv('YT_API_KEY')


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.constructor_title()

        self.response = self.constructor_pl()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.response['items']]

    def constructor_pl(self):
        """
        Возвращает информацию по плейлисту
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                 part='snippet, contentDetails',
                                                 maxResults=50,
                                                 ).execute()
        return playlists

    def constructor_title(self):
        """ Формирует название плейлиста как указано в задании """
        s = self.constructor_pl()['items'][1]['snippet']['title']
        s = s.split('/')[-1].strip()
        s1 = s.split(' ')
        title = f'{s1[0]}. {s1[-1]}'
        return title

    @property
    def total_duration(self):
        """ Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        """

        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        all_duration = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_duration = all_duration + duration
        return all_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """

        all_like_count = []
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()

        for video in video_response['items']:
            all_like_count.append(int(video['statistics']['likeCount']))

        video_like = dict(zip(self.video_ids, all_like_count))

        sorted_video_like = sorted(video_like.items(), key=lambda x: x[1], reverse=True)[0]

        return f"https://youtu.be/{sorted_video_like[0]}"

