from ..strategy import Strategy
from bs4 import BeautifulSoup
import requests


class HabrStrategy(Strategy):

    def parse(self, url: str) -> str:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise ValueError("Wrong URL")

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('meta', {'property': 'og:title'}).get('content')

        if title is None:
            return "No title"

        return title
