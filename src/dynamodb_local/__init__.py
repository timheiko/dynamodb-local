#!/usr/bin/env python3

import asyncio
from urllib import request
import shutil
from pathlib import Path
from os import makedirs, path
from hashlib import sha256

from logging import getLogger

__version__ = "1.0.0"

# https://pypi.org/project/pytest-dynamodb/
DYNAMODB_LOCAL_DIR = Path("tmp/dynamodb")

logger = getLogger(__name__)


def download_dynamodb(parent_dir: Path = DYNAMODB_LOCAL_DIR) -> None:
    tar_gz_url = (
        "https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz"
    )
    sha256_url = (
        "https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz.sha256"
    )
    tar_gz_filepath = parent_dir / "dynamodb.tar.gz"
    sha256_filepath = parent_dir / "dynamodb_local_latest.tar.gz.sha256"
    jar_file_name = "DynamoDBLocal.jar"

    if not check_sha26(
        tar_gz_filepath=tar_gz_filepath, sha256_filepath=sha256_filepath
    ):
        if path.exists(parent_dir):
            logger.debug(f"Cleaning up {parent_dir}")
            shutil.rmtree(parent_dir)

        logger.debug(f"Creating {parent_dir}")
        makedirs(parent_dir)

        logger.debug(f"Downloading DynamodDB to {parent_dir}")
        request.urlretrieve(tar_gz_url, tar_gz_filepath)
        shutil.unpack_archive(tar_gz_filepath, parent_dir)
        request.urlretrieve(sha256_url, sha256_filepath)

    return parent_dir / jar_file_name


def check_sha26(tar_gz_filepath: Path, sha256_filepath: Path) -> bool:
    if path.exists(tar_gz_filepath) and path.exists(sha256_filepath):
        logger.debug(
            f"Checking SHA256 of DynamoDB local archive: {sha256_filepath} {tar_gz_filepath}"
        )
        sha256_hash = sha256()
        with open(file=tar_gz_filepath, mode="rb") as file:
            for block in iter(lambda: file.read(4_096), b""):
                sha256_hash.update(block)

        sha256_digest = sha256_hash.hexdigest()

        with open(file=sha256_filepath, mode="r") as file:
            expected_sha256_digest = file.readline().strip().split()[0]
            return sha256_digest == expected_sha256_digest

    return False


async def download_dynamodb_async(
    parent_dir: Path = DYNAMODB_LOCAL_DIR,
    event_loop: "asyncio.EventLoop" = None,
):
    event_loop = event_loop or asyncio.get_running_loop()
    return await event_loop.run_in_executor(None, download_dynamodb, parent_dir)


if __name__ == "__main__":
    download_dynamodb_local()
