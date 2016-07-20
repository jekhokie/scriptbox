# start the application after importing all relative app components
from app import app
from random import randint
import requests
import time

# check if we are an injector - if so, we only need to fire off a request and terminate
if app.config['ROLE'] == 'Injector':
  while True:
    # create a random transaction ID
    transaction_id = randint(1, 1000000)

    # simulate being the first service in a pipeline to receive a request
    app.logger.info('Received Request', extra={'role': app.config['ROLE'], 'event': 'RECEIVED', 'transaction_id': transaction_id})

    # inject an artificial delay between 100-300ms into the cycle to simulate "processing"
    ms_delay = (randint(100, 300) / 1000.0)
    time.sleep(ms_delay)

    # record completing and passing the request downstream
    app.logger.info('Processed Request', extra={'role': app.config['ROLE'], 'event': 'PROCESSED', 'transaction_id': transaction_id})

    # send the transaction to the next service processor
    payload = {'transaction_id': transaction_id}
    requests.post(app.config['NEXT_HOP'], data=payload)
else:
  # else, start as a processor or terminator
  app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
