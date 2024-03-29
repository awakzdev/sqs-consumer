from flask import Flask, jsonify
from dotenv import load_dotenv
import boto3
import os
import time
import logging
import threading

'''
This script uses the Flask web framework and the AWS SDK for Python (Boto3)
to processes messages from an Amazon Simple Queue Service (SQS) queue.

The program creates a Flask app with two routes: '/' and '/count'.
The '/' route returns an HTTP OK response,
while the '/count' route returns the approximate number of messages in the SQS queue.
'''

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Create SQS client
sqs = boto3.client('sqs')
queue_url = os.getenv('SQS_QUEUE_URL')

def process_messages():
    '''
    Process SQS messages and deletes them after completion
    '''
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )

            message = response.get('Messages', [])[0]
            receipt_handle = message['ReceiptHandle']

            for x in range(6):
                logger.info('Processing message: %s, attempt: %d', message['Body'], x+1)
                time.sleep(5)

            # Delete the processed message from the queue
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            logger.info('Received and deleted message: %s', message)

        except (KeyError, IndexError):
            # No messages in the queue
            logger.info('No messages in the queue')
        
        time.sleep(10) # Wait 10 seconds before checking for new messages again

# Start message processing thread
message_thread = threading.Thread(target=process_messages)
message_thread.daemon = True
message_thread.start()

@app.route('/')
def test():
    '''
    Return an HTTP OK Response (200)
    '''
    return 'OK', 200

@app.route('/count')
def message_count():
    '''
    Return the number of messages within queue
    '''
    response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    return jsonify({'count': response['Attributes']['ApproximateNumberOfMessages']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
