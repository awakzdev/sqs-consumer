# sqs-worker

A sample application that connects to an sqs queue and processes a message by pulling it, sleeping for a while and deleting the message

## Config

The application accepts configuration via ENV vars.
Application uses boto, meaning any standard AWS credential methods are supported.

The following arguments are required:

SQS_QUEUE_URL - The URL of the SQS queue to pull from, in the form of https://sqs.{aws-region}.amazonaws.com/{aws-account-id}/{queue-name}


## Usage

Build the docker container
```
docker build . -t sqs-worker
```

Run with env file for configuration

```
docker run -it sqs-worker
```

sample .env file:
```
AWS_ACCESS_KEY_ID=ABCD1234ABC
AWS_SECRET_ACCESS_KEY=knsdf854ynldnbv9w459nbdb489
AWS_DEFAULT_REGION=eu-central-1
SQS_QUEUE_URL=https://sqs.eu-central-1.amazonaws.com/946796614687/processing-queue
```

## Endpoints
Support for Flask added within the following endpoints 
- ('/') will return an HTTP OK response 
- ('/count') will return the number of messages in the queue

## Keda (horizontal scaling) is included within /charts
Keda reads the amount of messages in queue through an attribute called `ApproximateNumberOfMessages` and scales your pods accordingly.

For more information on Keda you may view the URL provided - https://keda.sh/docs/2.9/deploy/
