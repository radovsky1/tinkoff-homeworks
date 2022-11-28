from typing import List


class Action:
    def __init__(self, from_version: int, to_version: int):
        self._from_version = from_version
        self._to_version = to_version

    @property
    def from_version(self):
        return self._from_version

    @property
    def to_version(self):
        return self._to_version

    def apply(self, text: str) -> str:
        raise NotImplementedError

    @property
    def text(self):
        raise NotImplementedError


class TextHistory:
    def __init__(self):
        self._text = ""
        self._version = 0
        self._actions: List[Action] = []

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version

    def insert(self, text: str, pos: int = None) -> int:
        if pos is None:
            pos = len(self._text)
        if pos > len(self._text) or pos < 0:
            raise ValueError

        old_version = self._version
        self._version += 1
        self._actions.append(
            InsertAction(old_version, self._version, pos, text)
        )
        self._text = self._text[:pos] + text + self._text[pos:]
        return self._version

    def replace(self, text: str, pos: int = None) -> int:
        if pos is None:
            pos = len(self._text)
        if pos > len(self._text) or pos < 0:
            raise ValueError

        old_version = self._version
        self._version += 1
        self._actions.append(
            ReplaceAction(old_version, self._version, pos, text)
        )
        self._text = self._text[:pos] + text + self._text[pos + len(text):]
        return self._version

    def delete(self, pos: int, length: int) -> int:
        if pos > len(self._text) or pos < 0:
            raise ValueError
        if length > len(self._text) or length < 0:
            raise ValueError
        if pos + length > len(self._text):
            raise ValueError

        old_version = self._version
        self._version += 1
        self._actions.append(
            DeleteAction(old_version, self._version, pos, length)
        )
        self._text = self._text[:pos] + self._text[pos + length:]
        return self._version

    def action(self, a: Action) -> int:
        if a.from_version != self._version:
            raise ValueError
        self._actions.append(a)
        self._text = a.apply(self._text)
        self._version = a.to_version
        return self._version

    @staticmethod
    def _merge_actions(actions: List[Action]) -> List[Action]:
        result: List[Action] = []
        for action in actions:
            if not result:
                result.append(action)
            elif isinstance(action, InsertAction) and isinstance(
                    result[-1], InsertAction
            ):
                if action.pos == result[-1].pos + len(result[-1].text):
                    result[-1] = InsertAction(
                        action.from_version,
                        action.to_version,
                        result[-1].pos,
                        result[-1].text + action.text,
                    )
                else:
                    result.append(action)
            elif isinstance(action, ReplaceAction) and isinstance(
                    result[-1], ReplaceAction
            ):
                if (
                        action.pos == result[-1].pos
                        and action.to_version == result[-1].to_version
                ):
                    result[-1] = ReplaceAction(
                        action.from_version,
                        action.to_version,
                        result[-1].pos,
                        result[-1].text + action.text,
                    )
                else:
                    result.append(action)
            elif isinstance(action, DeleteAction) and isinstance(
                    result[-1], DeleteAction
            ):
                if (
                        action.pos == result[-1].pos
                        and action.length == result[-1].length
                        and action.to_version == result[-1].to_version
                ):
                    result[-1] = DeleteAction(
                        action.from_version,
                        action.to_version,
                        result[-1].pos,
                        result[-1].length,
                    )
                else:
                    result.append(action)
            else:
                result.append(action)
        return result

    @staticmethod
    def _remove_opposite_actions(actions: List[Action]) -> List[Action]:
        result: List[Action] = []
        for action in actions:
            if not result:
                result.append(action)
            elif isinstance(action, InsertAction) and isinstance(
                    result[-1], DeleteAction
            ):
                if (
                        action.pos == result[-1].pos
                        and action.to_version == result[-1].from_version
                ):
                    result.pop()
                else:
                    result.append(action)
            elif isinstance(action, DeleteAction) and isinstance(
                    result[-1], InsertAction
            ):
                if (
                        action.pos == result[-1].pos
                        and action.to_version == result[-1].from_version
                ):
                    result.pop()
                else:
                    result.append(action)
            elif isinstance(action, ReplaceAction) and isinstance(
                    result[-1], ReplaceAction
            ):
                if (
                        action.pos == result[-1].pos
                        and action.to_version == result[-1].from_version
                ):
                    result.pop()
                else:
                    result.append(action)
            else:
                result.append(action)
        return result

    def get_actions(
            self, from_version: int = None, to_version: int = None
    ) -> List[Action]:
        if from_version is None:
            from_version = 0
        if to_version is None:
            to_version = self._version

        if from_version < 0 or from_version > self._version:
            raise ValueError
        if to_version < 0 or to_version > self._version:
            raise ValueError
        if from_version > to_version:
            raise ValueError

        actions = [
            action
            for action in self._actions
            if action.from_version >= from_version
               and action.to_version <= to_version
        ]

        actions = self._remove_opposite_actions(actions)
        actions = self._merge_actions(actions)

        return actions


class InsertAction(Action):
    def __init__(
            self, from_version: int, to_version: int, pos: int, text: str
    ):
        super().__init__(from_version, to_version)
        self._text = text
        self._pos = pos

    @property
    def text(self):
        return self._text

    @property
    def pos(self):
        return self._pos

    def apply(self, text: str) -> str:
        return text[: self._pos] + self._text + text[self._pos:]


class ReplaceAction(Action):
    def __init__(
            self, from_version: int, to_version: int, pos: int, text: str
    ):
        super().__init__(from_version, to_version)
        self._text = text
        self._pos = pos

    @property
    def text(self):
        return self._text

    @property
    def pos(self):
        return self._pos

    def apply(self, text: str) -> str:
        return (
                text[: self._pos]
                + self._text
                + text[self._pos + len(self._text):]
        )


class DeleteAction(Action):
    def __init__(
            self, from_version: int, to_version: int, pos: int, length: int
    ):
        super().__init__(from_version, to_version)
        self._pos = pos
        self._length = length

    @property
    def length(self):
        return self._length

    @property
    def pos(self):
        return self._pos

    def apply(self, text: str) -> str:
        return text[: self._pos] + text[self._pos + self._length:]
