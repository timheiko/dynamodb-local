import pytest
from dynamodb_local import download_dynamodb, download_dynamodb_async
from tempfile import TemporaryDirectory, mkdtemp
from pathlib import Path
from time import perf_counter


@pytest.fixture
def temp_directory() -> Path:
    tmpdirectory = TemporaryDirectory(prefix="dynamodb_local_")

    yield Path(tmpdirectory.name)

    return tmpdirectory.cleanup()


def test_download_dynamodb_fresh(temp_directory: Path):
    assert (
        download_dynamodb(parent_dir=temp_directory)
        == temp_directory / "DynamoDBLocal.jar"
    )


def test_download_dynamodb_cached(temp_directory: Path):
    download_dynamodb(parent_dir=temp_directory)

    t0 = perf_counter()
    assert (
        download_dynamodb(parent_dir=temp_directory)
        == temp_directory / "DynamoDBLocal.jar"
    )
    t1 = perf_counter()
    assert t1 - t0 < 1.0


@pytest.mark.asyncio
async def test_download_dynamodb_async_fresh(temp_directory: Path):
    assert (
        await download_dynamodb_async(parent_dir=temp_directory)
        == temp_directory / "DynamoDBLocal.jar"
    )


@pytest.mark.asyncio
async def test_download_dynamodb_async_cached(temp_directory: Path):
    await download_dynamodb_async(parent_dir=temp_directory)

    t0 = perf_counter()
    assert (
        await download_dynamodb_async(parent_dir=temp_directory)
        == temp_directory / "DynamoDBLocal.jar"
    )
    t1 = perf_counter()
    assert t1 - t0 < 1.0
