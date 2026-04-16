#!/usr/bin/env python3

import asyncio
import shutil
import socket
import subprocess
import time
from hashlib import sha256
from logging import getLogger
from os import PathLike, makedirs, path
from pathlib import Path
from urllib import request

__version__ = "1.1.6"

# https://pypi.org/project/pytest-dynamodb/
DYNAMODB_LOCAL_DIR = Path("tmp/dynamodb")

logger = getLogger(__name__)


def download_dynamodb(parent_dir: Path = DYNAMODB_LOCAL_DIR) -> None:
    parent_dir = Path(parent_dir or DYNAMODB_LOCAL_DIR)

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

        logger.debug(f"Downloading DynamoDB to {parent_dir}")
        request.urlretrieve(tar_gz_url, tar_gz_filepath)
        shutil.unpack_archive(tar_gz_filepath, parent_dir)
        request.urlretrieve(sha256_url, sha256_filepath)

    jar_path = parent_dir / jar_file_name
    logger.debug(f"jar path: {jar_path}")

    return jar_path


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


def start_dynamodb_local(
    *,
    java_executable: PathLike = None,
    disable_telemetry: bool = True,
    download: bool = True,
    parent_dir: PathLike = None,
    port: int = 8000,
):
    java_executable = java_executable or shutil.which("java")
    if not java_executable:
        raise DynamoDBLocalException("java executable not found!")

    disable_telemetry |= False
    dynamodb_local_jar = download_dynamodb(parent_dir=parent_dir)
    logger.debug(dynamodb_local_jar)

    args = [
        java_executable,
        "-jar",
        path.basename(dynamodb_local_jar),
        "-disableTelemetry" if disable_telemetry else "",
        "-port",
        str(port),
    ]
    logger.debug(args)

    proc = subprocess.Popen(
        args=args,
        cwd=Path(parent_dir).as_posix(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    host = "localhost"

    last_exception = None
    for _ in range(10):
        try:
            sock = socket.socket()
            sock.connect((host, port))
            break
        except (socket.error, socket.timeout) as e:
            last_exception = e
            time.sleep(0.5)
        finally:
            sock.close()
    else:
        raise DynamoDBLocalException from last_exception

    if (returncode := proc.poll()) is not None:
        raise DynamoDBLocalException(
            f"DynamoDB process has terminated unexpectedly, return code: {returncode}"
        )

    endpoint = f"http://{host}:{port}"

    logger.debug(f"DynamoDB local started at {endpoint}")

    return DynamoDBLocalServer(proc, endpoint=endpoint)


class DynamoDBLocalServer:
    def __init__(self, proc, endpoint: str):
        self.proc = proc
        self.endpoint = endpoint

    def __enter__(
        self,
    ):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()

    def shutdown(self):
        self.proc.terminate()


class DynamoDBLocalException(Exception):
    pass


if __name__ == "__main__":
    download_dynamodb()
