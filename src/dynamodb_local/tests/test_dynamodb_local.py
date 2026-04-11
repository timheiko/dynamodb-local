import pytest
from dynamodb_local import (
    download_dynamodb,
    download_dynamodb_async,
    start_dynamodb_local,
)
from tempfile import TemporaryDirectory, mkdtemp
from pathlib import Path
from time import perf_counter
from urllib import request
import time


@pytest.fixture
def tmp_directory() -> Path:
    tmp_dir = TemporaryDirectory(prefix="dynamodb_local_")

    yield Path(tmp_dir.name)

    return tmp_dir.cleanup()


def test_download_dynamodb_fresh(tmp_directory: Path):
    assert (
        download_dynamodb(parent_dir=tmp_directory)
        == tmp_directory / "DynamoDBLocal.jar"
    )


def test_download_dynamodb_cached(tmp_directory: Path):
    download_dynamodb(parent_dir=tmp_directory)

    t0 = perf_counter()
    assert (
        download_dynamodb(parent_dir=tmp_directory)
        == tmp_directory / "DynamoDBLocal.jar"
    )
    t1 = perf_counter()
    assert t1 - t0 < 1.0


@pytest.mark.asyncio
async def test_download_dynamodb_async_fresh(tmp_directory: Path):
    assert (
        await download_dynamodb_async(parent_dir=tmp_directory)
        == tmp_directory / "DynamoDBLocal.jar"
    )


@pytest.mark.asyncio
async def test_download_dynamodb_async_cached(tmp_directory: Path):
    await download_dynamodb_async(parent_dir=tmp_directory)

    t0 = perf_counter()
    assert (
        await download_dynamodb_async(parent_dir=tmp_directory)
        == tmp_directory / "DynamoDBLocal.jar"
    )
    t1 = perf_counter()
    assert t1 - t0 < 1.0


def test_start_dynamodb_local(tmp_directory: Path):
    with start_dynamodb_local(parent_dir=tmp_directory, port=8000) as dynamodb:
        endpoint = dynamodb.endpoint

        req = request.Request(endpoint, data=b"{}")
        req.add_header("Accept-Encoding", "identity")
        req.add_header(
            "Authorization",
            "AWS4-HMAC-SHA256 Credential=AKIAXXXXXXXXXXXXXXXX/20190505/ap-southeast-2/dynamodb/aws4_request, SignedHeaders=accept-encoding;cache-control;content-length;content-type;host;postman-token;user-agent;x-amz-date;x-amz-target, Signature=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        )
        req.add_header("Content-Type", "application/json")
        # https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ListTables.html
        req.add_header("X-Amz-Target", "DynamoDB_20120810.ListTables")
        req.add_header("X-Amz-Date", "20190505T235951Z")
        req.add_header("cache-control", "no-cache")

        with request.urlopen(req) as response:
            assert response.read().decode() == '{"TableNames":[]}'
