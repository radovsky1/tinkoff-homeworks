from unittest import TestCase

from golf import HitsMatch, HolesMatch, Player

from random import randrange


# additional tests
class HitsMatchAllWonTestCase(TestCase):

    def test_scenario(self):
        players_amount = randrange(2, 10)
        players = [Player(str(i)) for i in range(players_amount)]

        m = HitsMatch(players_amount, players)

        for _ in range(players_amount * players_amount - 1):
            m.hit(True)

        with self.assertRaises(RuntimeError):
            m.get_winners()

        m.hit(True)

        self.assertEqual(m.get_winners(), players)


class HolesMatchAllWonTestCase(TestCase):

    def test_scenario(self):
        players_amount = randrange(2, 10)
        players = [Player(str(i)) for i in range(players_amount)]

        m = HolesMatch(players_amount, players)

        for _ in range(players_amount * players_amount - 1):
            m.hit(True)

        with self.assertRaises(RuntimeError):
            m.get_winners()

        m.hit(True)

        self.assertEqual(m.get_winners(), players)


class HitsMatchAllMissedTestCase(TestCase):

    def test_scenario(self):
        players_amount = randrange(2, 20)
        players = [Player(str(i)) for i in range(players_amount)]

        m = HitsMatch(players_amount, players)

        for holes in range(players_amount):
            for _ in range(1, m.MAX_ATTEMPTS):
                for player in range(players_amount):
                    m.hit()

        self.assertEqual(m.get_winners(), players)

        table = m.get_table()
        for row in table[1:]:
            for cell in row:
                self.assertEqual(cell, m.MAX_ATTEMPTS)


class HolesMatchAllMissedTestCase(TestCase):

    def test_scenario(self):
        players_amount = randrange(2, 20)
        players = [Player(str(i)) for i in range(players_amount)]

        m = HolesMatch(players_amount, players)

        for holes in range(players_amount):
            for _ in range(m.MAX_ATTEMPTS):
                for player in range(players_amount):
                    m.hit()

        self.assertEqual(m.get_winners(), players)

        table = m.get_table()
        for row in table[1:]:
            for cell in row:
                self.assertEqual(cell, 0)
