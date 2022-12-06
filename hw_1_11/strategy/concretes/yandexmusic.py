from ..strategy import Strategy
from bs4 import BeautifulSoup
import requests
import json


class YandexmusicStrategy(Strategy):

    def parse(self, url: str) -> str:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise ValueError("Wrong URL")

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            light_data = json.loads(soup.find(class_="light-data").text)
        except AttributeError:
            return "No title"

        return light_data["name"]
