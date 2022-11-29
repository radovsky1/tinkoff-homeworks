import abc

from typing import List
from hw_1_12.repository import RepositoryInterface
from .webapi import DistributedFileStorage


class ServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_file(self, file_name: str) -> str:
        pass


class Service(ServiceInterface):
    def __init__(
        self,
        repository: RepositoryInterface,
        file_storages: List[DistributedFileStorage],
        save_files: bool = True,
    ):
        self.repository = repository
        self.file_storages = file_storages
        self.save_files = save_files

    async def get_file(self, file_name: str) -> str:
        try:
            return await self.repository.get_file(file_name)
        except FileNotFoundError:
            for file_storage in self.file_storages:
                try:
                    file_content = await file_storage.get(file_name)
                except FileNotFoundError:
                    continue
                if self.save_files:
                    await self.repository.save_file(file_name, file_content)
                return file_content
            raise FileNotFoundError
