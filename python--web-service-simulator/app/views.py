from app import app
from flask import request
from random import randint
import requests
import time

# default path
@app.route("/{}".format(app.config['LISTEN_PATH']), methods=['POST'])
def handler():
  # get the incoming transaction ID
  transaction_id = request.form['transaction_id']

  # record receiving the request
  app.logger.info('Received Request', extra={'role': app.config['ROLE'], 'event': 'RECEIVED', 'transaction_id': transaction_id})

  # inject an artificial delay between 100-300ms into the cycle to simulate "processing"
  ms_delay = (randint(100, 300) / 1000.0)
  time.sleep(ms_delay)

  # record completing and passing the request downstream
  app.logger.info('Processed Request', extra={'role': app.config['ROLE'], 'event': 'PROCESSED', 'transaction_id': transaction_id})

  # if we are a processor, forward the transaction to the next service processor in line
  # we don't care about a response for the purposes of this example application - ignore it
  if app.config['ROLE'] == 'Processor':
    payload = {'transaction_id': transaction_id}
    requests.post(app.config['NEXT_HOP'], data=payload)

  return "TRANSACTION ID '{}' PROCESSED".format(transaction_id), 201
