from hw_1_11.strategy import YandexmusicStrategy


def test_yandexmusic_strategy():
    strategy = YandexmusicStrategy()
    assert strategy.parse('https://music.yandex.ru/album/13707793/track/60292250') == 'Blinding Lights'


def test_yandexmusic_strategy2():
    strategy = YandexmusicStrategy()
    assert strategy.parse('https://music.yandex.ru/album/13707793/track/24103918') == 'Can\'t Feel My Face'
