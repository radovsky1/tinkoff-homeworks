import pytest
from unittest.mock import AsyncMock

from hw_1_12.service import Service


@pytest.mark.asyncio
async def test_get_file(mocker):
    repository = AsyncMock()
    repository.get_file.return_value = "file_content"
    service = Service(repository, [])
    assert await service.get_file("file_name") == "file_content"
    repository.get_file.assert_awaited_once_with("file_name")


@pytest.mark.asyncio
async def test_get_file_not_found():
    repository = AsyncMock()
    repository.get_file.side_effect = FileNotFoundError
    service = Service(repository, [])
    with pytest.raises(FileNotFoundError):
        await service.get_file("file_name")
    repository.get_file.assert_awaited_once_with("file_name")


@pytest.mark.asyncio
async def test_get_file_from_storage():
    repository = AsyncMock()
    repository.get_file.side_effect = FileNotFoundError
    file_storage = AsyncMock()
    file_storage.get.return_value = "file_content"
    service = Service(repository, [file_storage])
    assert await service.get_file("file_name") == "file_content"
    repository.get_file.assert_awaited_once_with("file_name")
    file_storage.get.assert_awaited_once_with("file_name")
    repository.save_file.assert_awaited_once_with("file_name", "file_content")


@pytest.mark.asyncio
async def test_get_file_from_storage_not_found():
    repository = AsyncMock()
    repository.get_file.side_effect = FileNotFoundError
    file_storage = AsyncMock()
    file_storage.get.side_effect = FileNotFoundError
    service = Service(repository, [file_storage])
    with pytest.raises(FileNotFoundError):
        await service.get_file("file_name")
    repository.get_file.assert_awaited_once_with("file_name")
    file_storage.get.assert_awaited_once_with("file_name")
    repository.save_file.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_file_with_save_files_true():
    repository = AsyncMock()
    repository.get_file.side_effect = FileNotFoundError
    file_storage = AsyncMock()
    file_storage.get.return_value = "file_content"
    service = Service(repository, [file_storage], save_files=True)
    assert await service.get_file("file_name") == "file_content"
    repository.get_file.assert_awaited_once_with("file_name")
    file_storage.get.assert_awaited_once_with("file_name")
    repository.save_file.assert_awaited_once_with("file_name", "file_content")
