=========================
DynamoDB local downloader
=========================

Getting Started
---------------

1. Install the library

.. code-block:: bash

    % python3 -m pip install dynamodb_local

2. Usage

Non-async DynamoDB local download:

.. code-block:: python

    from dynamodb_local import download_dynamodb
    ...
    dynamodb_local_jar_path = download_dynamodb()

Async DynamoDB local download:

.. code-block:: python

   from dynamodb_local import download_dynamodb_async
   ...
   dynamodb_local_jar_path = await download_dynamodb_async()

Starting DynamoDB local endpoint:

.. code-block:: python

   from dynamodb_local import download_dynamodb_async
   ...
   dynamodb_local_dir = ...
   
   dynamodb_local_jar_path = await download_dynamodb_async(dynamodb_local_dir)

   with start_dynamodb_local(parent_dir=dynamodb_local_dir, port=8000) as dynamodb:
        endpoint = dynamodb.endpoint

        # the endpoint is ready to be sent requests to, e.g. through boto3 SDK


Features
--------
* Downloads `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_ archive and unpacks it to a given parent directory.
* Prevents redundant downloading of `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_ on every run by verifying the downloaded local version against its `sha256 digest <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz.sha256>`_.
* No external dependencies.

Notes
-----
* The library downloads and unpacks `DynamoDB local <https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_latest.tar.gz>`_.
* The library can start a DynamoDB local instance; however, it requires a JRE or JDK for that.

Credits
-------
* `DynamoDBLocal Deploying DynamoDB locally on your computer <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html#DynamoDBLocal.DownloadingAndRunning.title>`_.
