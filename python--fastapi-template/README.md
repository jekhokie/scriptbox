# Python FastAPI Template

Quick template project that gets a decent starting point for the Python FastAPI framework.

## Install

```bash
$ python3 -m virtualenv .env
$ . .env/bin/activate
$ pip install -r requirements.lock
```

## Configure Settings

```bash
$ cp config/settings.yaml.sample config/settings.yaml
$ vim config/settings.yaml
# edit settings
$ chmod 600 config/settings.yaml
```

## Create and Configure Database

TODO: Make seed starter/bootstrap out of this.

```bash
$ sqlite3 db/fastapi-test.db

$ CREATE TABLE cars(id int not null, year int, make varchar(255), model varchar(255), primary key (id));
$ INSERT INTO cars (id, year, make, model) values (1, 2019, "Honda", "Civic");
$ INSERT INTO cars (id, year, make, model) values (2, 2015, "Toyota", "Prius");

$ CREATE TABLE boats(id int not null, year int, make varchar(255), length_ft int, primary key (id));
$ INSERT INTO boats (id, year, make, length_ft) values (1, 2019, "Robalo", "24");
$ INSERT INTO boats (id, year, make, length_ft) values (2, 2019, "Sea Ray", "18");
```

## Run

```bash
$ uvicorn python__fastapi_template.main:app --reload
```

Visit the following URLs in a browser:

  * [http://localhost:8080](http://localhost:8080).
  * [http://localhost:8080/api/docs](http://localhost:8080/api/docs).
  * [http://localhost:8080/api/spec](http://localhost:8080/api/spec).
