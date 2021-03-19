#!/usr/bin/env python3
#
# Purpose: Start a Kafka consumer which will consume messages
#          from a configured topic.
#
# Example Usage:
#   python3 start_consumer.py

import signal
import sys
import yaml
from kafka import KafkaConsumer, TopicPartition

print('Starting consumer...')

def handle_terminate(sig, frame):
    '''
    Terminate the script when CTRL-C is pressed.
    '''
    print('SIGINT received - terminating')
    sys.exit(0)

# ensure terminate (SIGINT) can be handled
signal.signal(signal.SIGINT, handle_terminate)

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

def main():
    '''
    Main execution loop for consuming messages - can be terminated
    by issuing SIGINT (CTRL-C).
    '''

    # set up consumer, assign to consumer group and partition list (partition 1)
    consumer = KafkaConsumer(config['topic'], bootstrap_servers=config['bootstrap-server'], group_id='test_consumer_group')

    while True:
        print('Waiting for message...')
        w = next(consumer)
        print('Consumed "{}"'.format(w.value.decode()))

if __name__ == '__main__':
    main()
