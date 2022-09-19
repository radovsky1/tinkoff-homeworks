class Player:

    def __init__(self, name: str) -> None:
        self.name = name


class Match:
    MAX_ATTEMPTS = 10

    def __init__(self, holes: int, players: [Player]) -> None:
        self.holes = holes
        self.players = players
        self.finished = False
        self._cur_hole = 0
        self._cur_player = 0
        self._attempt = 1
        self._table = []
        for i in range(holes):
            self._table.append([None for _ in range(len(players))])

    def _next_hole(self):
        pass

    def hit(self, success=False):
        pass

    def get_winners(self) -> [Player]:
        pass

    def get_table(self) -> list:
        names_row = [tuple(player.name for player in self.players)]
        return names_row + [tuple(t) for t in self._table]

    def _get_points(self, player_id: int) -> int:
        return sum(self._table[i][player_id] for i in range(self.holes))


class HitsMatch(Match):

    def __init__(self, holes, players: [Player]) -> None:
        super().__init__(holes, players)

    def _next_hole(self):
        self._cur_hole += 1
        self._cur_player = self._cur_hole
        self._attempt = 1

        if self._cur_hole == self.holes:
            self.finished = True

    def hit(self, success=False):
        if self.finished:
            raise RuntimeError('Match is finished')

        if success:
            self._table[self._cur_hole][self._cur_player] = self._attempt

            if self._table[self._cur_hole].count(None) == 0:
                self._next_hole()
                return

        while True:
            self._cur_player += 1
            if self._cur_player == len(self.players):
                self._cur_player = 0
            if self._cur_player == self._cur_hole:
                self._attempt += 1

            if self._table[self._cur_hole][self._cur_player] is None:
                break

        if self._attempt == self.MAX_ATTEMPTS:
            for i, value in enumerate(self._table[self._cur_hole]):
                if value is None:
                    self._table[self._cur_hole][i] = self.MAX_ATTEMPTS
            self._next_hole()

    def get_winners(self) -> [Player]:
        if not self.finished:
            raise RuntimeError('Match is not finished')

        total_points = [self._get_points(i) for i in range(len(self.players))]
        min_points = min(total_points)

        winners = []
        for i, points in enumerate(total_points):
            if points == min_points:
                winners.append(self.players[i])
        return winners


class HolesMatch(Match):

    def __init__(self, holes: int, players: [Player]) -> None:
        super().__init__(holes, players)

    def _next_hole(self):
        for i, value in enumerate(self._table[self._cur_hole]):
            if value is None:
                self._table[self._cur_hole][i] = 0

        self._cur_hole += 1
        self._cur_player = self._cur_hole
        self._attempt = 1

        if self._cur_hole == self.holes:
            self.finished = True

    def hit(self, success=False):
        if self.finished:
            raise RuntimeError('Match is finished')

        if success:
            self._table[self._cur_hole][self._cur_player] = 1

        while True:
            self._cur_player += 1
            if self._cur_player == len(self.players):
                self._cur_player = 0

            if self._cur_player == self._cur_hole:
                if self._table[self._cur_hole].count(1) > 0:
                    self._next_hole()
                    break
                else:
                    self._attempt += 1

            if self._table[self._cur_hole][self._cur_player] is None:
                break

        if self._attempt == self.MAX_ATTEMPTS + 1:
            self._next_hole()

    def get_winners(self) -> [Player]:
        if not self.finished:
            raise RuntimeError('Match is not finished')

        total_points = [self._get_points(i) for i in range(len(self.players))]
        max_points = max(total_points)

        winners = []
        for i, points in enumerate(total_points):
            if points == max_points:
                winners.append(self.players[i])
        return winners
