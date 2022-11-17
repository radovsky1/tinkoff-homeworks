import abc

from hw_1_10.tvmaze import search


class ServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_program_info(self, program_name):
        pass


class Service(ServiceInterface):

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
