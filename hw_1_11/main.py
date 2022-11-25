from strategy import Context, Strategy, YoutubeStrategy, HabrStrategy, YandexmusicStrategy
from enum import Enum


class URLPatterns(Enum):
    YOUTUBE = 'https://www.youtube.com/watch?v='
    YANDEXMUSIC = 'https://music.yandex.ru/album/'
    HABR = 'https://habr.com/ru/post/'


def select_strategy(url: str) -> Strategy:
    if URLPatterns.YOUTUBE.value in url:
        return YoutubeStrategy()
    elif URLPatterns.HABR.value in url:
        return HabrStrategy()
    elif URLPatterns.YANDEXMUSIC.value in url:
        return YandexmusicStrategy()
    else:
        raise ValueError('Unsupported site')


if __name__ == '__main__':
    url = input('Enter url: ')
    strategy = select_strategy(url)
    context = Context(strategy)
    print(context.parse(url))
