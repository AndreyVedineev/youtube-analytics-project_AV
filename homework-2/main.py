from src.channel import Channel

if __name__ == '__main__':
    office = Channel('UC1eFXmJNkjITxPFWTy6RsWg')

    # получаем значения атрибутов
    print(office.title)  # Редакция
    print(office.video_count)  # 620 (может уже больше)
    print(office.url)  # https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA

    # менять не можем
    office.channel_id = 'Новое название'
    # AttributeError: property 'channel_id' of 'Channel' object has no setter
    print(office.channel_id)

    # можем получить объект для работы с API вне класса
    print(Channel.get_service())
    # <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

    # создаем файл 'office.json' в данными по каналу
    office.to_json('office.json')
