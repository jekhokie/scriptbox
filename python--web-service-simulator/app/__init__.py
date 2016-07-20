from flask import Flask

# construct the application object and apply configurations to the environment
# setting "instance_relative_config=True" loads the configuration from the 'instance' folder
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# make sure that the role specified for this instance is something that is recognized
valid_roles = ['Injector', 'Processor', 'Terminator']
if app.config['ROLE'] not in valid_roles:
  raise ValueError("The role specified in the configuration '{}' is not valid - must be one of '{}'".format(app.config['ROLE'], valid_roles))

# load routes/views
from app import views
