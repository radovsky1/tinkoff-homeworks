from unittest import TestCase

from datetime import datetime

from log_parse import parse_date


class TestCaseParseDateOK(TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("[18/Mar/2018 11:19:40]"),
                         datetime(2018, 3, 18, 11, 19, 40))


class TestCaseParseDateError(TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("18/Mar/2018 11:19:40]"), None)
