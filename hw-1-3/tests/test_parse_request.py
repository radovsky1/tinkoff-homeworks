from unittest import TestCase

from datetime import datetime

from log_parse import parse_request


class TestCaseParseRequestOK(TestCase):
    def test_parse_request(self):
        self.assertEqual(parse_request("GET https://api/v2/banner/25019354.jpg HTTP/1.1"),
                         ('api/v2/banner/25019354.jpg', 'GET', 'HTTP/1.1'))


class TestCaseParseRequestError(TestCase):
    def test_parse_request(self):
        self.assertEqual(parse_request("GET https://api/v2/banner/25019354.jpg"), None)


class TestCaseParseRequestError2(TestCase):
    def test_parse_request(self):
        self.assertEqual(parse_request("https://api/v2/banner/25019354.jpg"), None)