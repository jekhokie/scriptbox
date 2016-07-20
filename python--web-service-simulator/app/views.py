from app import app
from random import randint
import time

# default path
@app.route("/{}".format(app.config['LISTEN_PATH']), methods=['POST'])
def handler():
  # record receiving the request
  app.logger.info('Received Request', extra={"event": "RECEIVED", "transaction_id": "123"})

  # inject an artificial delay between 100-300ms into the cycle to simulate "processing"
  ms_delay = (randint(100, 300) / 1000.0)
  time.sleep(ms_delay)

  # record completing and passing the request downstream
  app.logger.info('Processed Request', extra={"event": "PROCESSED", "transaction_id": "123"})

  return 'HERE', 201
