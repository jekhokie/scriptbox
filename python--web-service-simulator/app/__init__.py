from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

# construct the application object and apply configurations to the environment
# setting "instance_relative_config=True" loads the configuration from the 'instance' folder
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# set up logging
app.logger.setLevel(logging.INFO)

# configuration validation
# make sure that the role specified for this instance is something that is recognized
valid_roles = ['Injector', 'Processor', 'Terminator']
if app.config['ROLE'] not in valid_roles:
  raise ValueError("The role specified in the configuration '{}' is not valid - must be one of '{}'".format(app.config['ROLE'], valid_roles))

# create a service log directory if one does not yet exist
# this is useful if you wish to run multiple services on the same host
log_directory = "logs/{}".format(app.config['LISTEN_PATH'])
if not os.path.exists(log_directory):
  os.makedirs(log_directory)

# set up the custom log to record transaction IDs
log_file = "{}/{}.log".format(log_directory, app.config['LISTEN_PATH'])
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(role)s - %(event)s - Trans. ID [%(transaction_id)s] - %(message)s")
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=20)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# load routes/views
from app import views
