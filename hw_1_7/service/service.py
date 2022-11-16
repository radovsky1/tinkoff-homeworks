import abc

from hw_1_7.filedict import FileDict
from hw_1_7.tvmaze import search


class ServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_program_info(self, program_name):
        pass

    @abc.abstractmethod
    def add_to_favorites(self, program_name):
        pass

    @abc.abstractmethod
    def remove_from_favorites(self, program_name):
        pass

    @abc.abstractmethod
    def get_favorites(self):
        pass


class Service(ServiceInterface):
    def __init__(self, filedict: FileDict):
        self._filedict = filedict

    def get_program_info(self, program_name: str) -> str:
        try:
            program = search(program_name)
        except ValueError:
            return "Bad request"
        if program is None:
            return "No results found"
        return (
            "Name: {}\n"
            "Network Name: {}\n"
            "Network Country Name: {}\n"
            "Summary: {}".format(
                program.name,
                program.network.name,
                program.network.country.name,
                program.summary,
            )
        )

    def add_to_favorites(self, program_name: str) -> str:
        if program_name in self._filedict:
            return "This program is already in favorites"
        self._filedict[program_name] = "1"
        return "Program added to favorites"

    def remove_from_favorites(self, program_name: str) -> str:
        try:
            del self._filedict[program_name]
            return "Program removed from favorites"
        except KeyError:
            return "This program is not in favorites"

    def get_favorites(self) -> str:
        if not self._filedict:
            return "Favorites is empty"
        return "\n".join(self._filedict.keys())
