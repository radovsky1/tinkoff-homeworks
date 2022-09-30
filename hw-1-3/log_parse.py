# -*- encoding: utf-8 -*-

from datetime import datetime


class ParserConstants(object):
    RETURNING_LIMIT = 5


def is_date_valid(date: datetime,
                  start_at: str = None,
                  stop_at: str = None) -> bool:
    if start_at:
        start_at = datetime.strptime(start_at, '%d/%b/%Y %H:%M:%S')
        if date < start_at:
            return False
    if stop_at:
        stop_at = datetime.strptime(stop_at, '%d/%b/%Y %H:%M:%S')
        if date > stop_at:
            return False
    return True


def parse_date(block: str):
    try:
        date = block.split('[')[1].split(']')[0]
    except IndexError as e:
        print('Error while parsing: ', e)
        return None
    else:
        date = datetime.strptime(date, '%d/%b/%Y %H:%M:%S')

    return date


def parse_request(block: str):
    try:
        request_type = block.split(' ')[0]
        request = block.split(' ')[1].split('?')[0].split("//")[1]
        protocol = block.split(' ')[2]
    except IndexError as e:
        print('Error while parsing: ', e)
        return None
    else:
        return request, request_type, protocol


def parse(
        log_file: str = "log.log",
        ignore_files: bool = False,
        ignore_urls: list = None,
        start_at: str = None,
        stop_at: str = None,
        request_type: str = None,
        ignore_www: bool = False,
        slow_queries: bool = False
):
    if ignore_urls is None:
        ignore_urls = []

    with open(log_file, 'r') as file:
        lines = file.readlines()

    response_time: dict[str, int] = {}
    frequency: dict[str, int] = {}

    for line in lines:
        if line[0] != '[':
            continue

        blocks = line.split('"')
        if len(blocks) != 3:
            continue

        # date
        date = parse_date(blocks[0])
        if not is_date_valid(date, start_at, stop_at):
            continue

        # request
        request, rtype, protocol = parse_request(blocks[1])

        if request_type and rtype != request_type:
            continue

        if ignore_www:
            request = request.replace('www.', '')

        if ignore_urls and request in ignore_urls:
            continue

        if ignore_files:
            request_blocks = request.split('/')
            if len(request_blocks) > 1 and '.' in request_blocks[-1]:
                continue

        if slow_queries:
            query_time = int(blocks[2].split(' ')[-1])
            response_time[request] = response_time.get(request, 0) + query_time

        frequency[request] = frequency.get(request, 0) + 1

    if not slow_queries:
        urls_frequency = []
        for url, count in frequency.items():
            urls_frequency.append(count)
        urls_frequency.sort(reverse=True)

        return urls_frequency[:ParserConstants.RETURNING_LIMIT]
    else:
        urls_response_time = []
        for url, time in response_time.items():
            urls_response_time.append(time // frequency[url])
        urls_response_time.sort(reverse=True)

        return urls_response_time[:ParserConstants.RETURNING_LIMIT]
