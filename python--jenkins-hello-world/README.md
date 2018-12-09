# Jenkins Hello World

This is a very small Python application that can be used for testing a Jenkins pipeline (starter
project). It is a Python Flask web application that has PyTest Unit tests built in to exercise
the CI portions of Jenkins.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--jenkins-hello-world/
```

Install the required environment and libraries:

```bash
$ virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Tests

You can run the PyTest test suite using the following command, which by default should succeed:

```bash
$ python -m pytest tests/test_app.py
```

## Starting the Application

To start the application perform the following:

```bash
$ python run.py
```

Following startup, you should be able to visit the following URL and see the Hello World example
output printed in your browser (assuming this is running on your local machine):

[http://localhost:80/](http://localhost:80/)
