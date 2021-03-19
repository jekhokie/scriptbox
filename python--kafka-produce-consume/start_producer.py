#!/usr/bin/env python3
#
# Purpose: Start a Kafka producer which will publish random
#          words/messages to a configured topic every 1 second.
#
# Example Usage:
#   python3 start_producer.py

import random
import signal
import sys
import time
import yaml
from kafka import KafkaProducer

print('Starting producer...')

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
    Main execution loop for producing messages - can be terminated
    by issuing SIGINT (CTRL-C).
    '''

    # set up some variables, and get the word list for random publishing
    rwords = open('config/wordlist.txt').read().splitlines()
    producer = KafkaProducer(bootstrap_servers=config['bootstrap-server'])

    # loop and publish random words every 1 second
    while True:
        w1 = random.choice(rwords)
        w2 = random.choice(rwords)
        rw = '{} {}'.format(w1, w2)

        print('Publishing "{}"'.format(rw))
        producer.send(config['topic'], str.encode(rw))
        time.sleep(1)

if __name__ == '__main__':
    main()
