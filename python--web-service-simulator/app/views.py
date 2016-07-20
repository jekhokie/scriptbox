from app import app

# default path
@app.route("/{}".format(app.config['LISTEN_PATH']), methods=['GET', 'POST'])
def handler():
  return 'HERE', 201
