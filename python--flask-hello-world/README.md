# Flask Hello World

This project is intended to be a starting point for a basic Hello World Python Flask application
that I repeatedly revisit for many proof of concept projects.

## Prerequisites

Install easy_install, pip and virtualenv. Then, clone this repository and navigate to this example:

```bash
$ git clone https://<git_location>/scriptbox.git
$ cd scriptbox/python--flask-hello-world
```

Install the required environment and libraries:

```bash
$ virtualenv --no-site-packages --distribute .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Usage

To start the Flask application, simply run the `run.py` script:

```bash
$ python run.py
```

You can now open a browser and navigate to http://<SERVER_IP>:8000/ to see the Hello World Flask
basic website.
