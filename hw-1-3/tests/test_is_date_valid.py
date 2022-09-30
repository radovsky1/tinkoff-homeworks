from unittest import TestCase

from datetime import datetime

from log_parse import is_date_valid


class TestIsDateValidTrue(TestCase):
    def test_is_date_valid(self):
        self.assertTrue(
            is_date_valid(datetime.strptime("18/Mar/2018 11:19:40", "%d/%b/%Y %H:%M:%S"), "18/Mar/2018 11:19:40",
                          "18/Mar/2018 11:19:40"))


class TestIsDateValidFalse(TestCase):
    def test_is_date_valid(self):
        self.assertFalse(
            is_date_valid(datetime.strptime("18/Mar/2018 11:19:40", "%d/%b/%Y %H:%M:%S"), "18/Mar/2018 11:19:41",
                          "18/Mar/2018 11:19:42"))
