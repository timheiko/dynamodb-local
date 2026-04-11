=========================
DynamoDB local downloader
=========================

Getting Started
---------------

1. Install the library

.. code-block:: bash

    % python3 -m pip install dynamodb_local

2. Usage

Non-async

.. code-block:: python

    from dynamodb_local import download_dynamodb
    ...
    dynamodb_local_jar_path = download_dynamodb()

Async

.. code-block:: python

   from dynamodb_local import download_dynamodb_async
   ...
   dynamodb_local_jar_path = await download_dynamodb_async()

Features
--------
* Downloads `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_ archive and unpacks it to a given parent directory.
* Prevents redundant downloading of `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_ on every run by verifying the downloaded local version against its `sha256 digest <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz.sha256>`_.
* No external dependencies.

Notes
-----
* This library does not Starting the `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_ it downloaded and unpacked.
* Starting the actual DynamoDB lolal process requieres a JRE or JDK.


Credits
-------
* `DynamoDBLocal Deploying DynamoDB locally on your computer <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html#DynamoDBLocal.DownloadingAndRunning.title>`_.