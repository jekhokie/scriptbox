# Python FastAPI Template

Quick template project that gets a decent starting point for the Python FastAPI framework.

## Install

```bash
$ python3 -m virtualenv .env
$ . .env/bin/activate
$ pip install -r requirements.lock
```

## Configure

```bash
$ cp config/settings.yaml.sample config/settings.yaml
$ vim config/settings.yaml
# edit settings
$ chmod 600 config/settings.yaml
```

## Run

```bash
$ uvicorn python__fastapi_template.main:app --reload
```

Visit the following URL in the browser: [http://localhost:8080](http://localhost:8080).
