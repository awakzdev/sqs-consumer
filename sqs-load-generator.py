import boto3
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

'''
The function of the program takes an optional argument (the number of messages to send)
from the command line and sends that number of messages to the SQS queue.
'''

# Load environment variables from .env
load_dotenv()

# Create a session and client for the SQS service
session = boto3.Session()
sqs_client = session.client('sqs')

def send_sqs_message(queue_url, message):
    '''
    Defines the message of the body by including a string
    with the message number, current date and time.
    '''
    date_time = datetime.now()
    response = sqs_client.send_message(
        QueueUrl=os.getenv('SQS_QUEUE_URL'),
        MessageBody=("This was sent on: " + str(date_time.strftime('%Y-%m-%d %H:%M:%S')))
    )
    return response

def main():
    '''
    Processes the message and sends it to SQS URL.
    Multiple messages may be sent by using 'python -m sqs-load-generator.py <number-of-messages>' (default 1)
    '''
    queue_url = os.getenv('SQS_QUEUE_URL')
    num_messages = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(num_messages):
        message = 'This is message {}'.format(i + 1)
        response = send_sqs_message(queue_url, message)
        print('Sent message: {}'.format(response['MessageId']))

if __name__ == '__main__':
    main()