from app import app
from flask import request
from random import randint
import time

# default path
@app.route("/{}".format(app.config['LISTEN_PATH']), methods=['POST'])
def handler():
  # get the incoming transaction ID
  transaction_id = request.form['transaction_id']

  # record receiving the request
  app.logger.info('Received Request', extra={"event": "RECEIVED", "transaction_id": transaction_id})

  # inject an artificial delay between 100-300ms into the cycle to simulate "processing"
  ms_delay = (randint(100, 300) / 1000.0)
  time.sleep(ms_delay)

  # record completing and passing the request downstream
  app.logger.info('Processed Request', extra={"event": "PROCESSED", "transaction_id": transaction_id})

  return "TRANSACTION ID '{}' PROCESSED".format(transaction_id), 201
