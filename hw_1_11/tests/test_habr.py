import pytest
from hw_1_11.strategy import HabrStrategy


def test_habr_strategy():
    strategy = HabrStrategy()
    assert strategy.parse('https://habr.com/ru/post/280238/') == 'Web Scraping с помощью python'


def test_habr_strategy_with_wrong_url():
    strategy = HabrStrategy()
    assert strategy.parse('https://habr.com/ru/post/549512') == "Хабр"
