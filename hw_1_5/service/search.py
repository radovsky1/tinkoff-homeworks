import requests
import json

from .model import TVProgram
from .filedict import FileDict
from functools import wraps
from datetime import datetime
from typing import Callable, Optional


class TVMazeConstants(object):
    SHOWS_ENDPOINT = "https://api.tvmaze.com/singlesearch/shows?q="
    TIMEOUT = 10  # seconds


def get_response(query: str) -> dict:
    response = requests.Response()
    try:
        response = requests.get(
            TVMazeConstants.SHOWS_ENDPOINT + query,
            timeout=TVMazeConstants.TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred: ", err)
    except requests.exceptions.ConnectionError as err:
        print("Connection error occurred: ", err)
    except requests.exceptions.Timeout as err:
        print("Timeout error occurred: ", err)
    except requests.exceptions.RequestException as err:
        print("Request error occurred: ", err)
    finally:
        return response.json()


def cache(ttl: int) -> Callable:
    """Decorator that caches the results of the function call.

    :param ttl:
    :return:
    """

    cache_data = FileDict("cache")

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_result = cache_data.get(args[0])

            if cached_result is not None:
                cached_result = json.loads(cached_result)
                cached_timestamp = float(cached_result["timestamp"])
                if datetime.now().timestamp() - cached_timestamp <= ttl:
                    return TVProgram.parse_obj(cached_result)

            result = func(*args, **kwargs)
            cache_data[result.name] = json.dumps(
                result.dict()
                | {"timestamp": datetime.now().timestamp()}
                | {"ttl": ttl}
            )
            return result

        return wrapper

    return decorator


@cache(ttl=10)
def search(query: str) -> Optional[TVProgram]:
    response = get_response(query)
    try:
        return TVProgram(**response)
    except ValueError as err:
        print("Value error occurred: ", err)
        return None
