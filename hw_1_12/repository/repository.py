import abc


class RepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_file(self, file_name: str) -> str:
        pass

    @abc.abstractmethod
    async def save_file(self, file_name: str, file_content: str) -> None:
        pass


class Repository(RepositoryInterface):
    def __init__(self, directory: str):
        self.directory = directory

    async def get_file(self, file_name: str) -> str:
        with open(f"{self.directory}/{file_name}", "r") as f:
            return f.read()

    async def save_file(self, file_name: str, content: str) -> None:
        with open(f"{self.directory}/{file_name}", "w") as f:
            f.write(content)
