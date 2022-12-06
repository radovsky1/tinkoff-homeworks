from hw_1_11.strategy import YoutubeStrategy


def test_youtube_strategy():
    strategy = YoutubeStrategy()
    assert strategy.parse(
        'https://www.youtube.com/watch?v=4m1EFMoRFvY') == 'Beyoncé - Single Ladies (Put a Ring on It) (Video Version)'


def test_youtube_strategy2():
    strategy = YoutubeStrategy()
    assert strategy.parse('https://www.youtube.com/watch?v=mHXEJuaTPc8') == 'ХОЛМС ОЖИЛ ► The Devil in Me #3'
