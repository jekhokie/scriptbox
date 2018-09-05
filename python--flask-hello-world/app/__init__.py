import os
from flask import Flask
import socket

app = Flask(__name__)

# a simple page that says hello
@app.route('/')
def hello():
    html = "<h3>Hello World from {hostname}!</h3>"
    return html.format(hostname=socket.gethostname())
