from app import app

# default path
@app.route("/{}".format(app.config['LISTEN_PATH']), methods=['GET', 'POST'])
def handler():
  app.logger.info('Received Request', extra={"transaction_id": "123"})
  return 'HERE', 201
