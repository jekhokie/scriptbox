# NodeJS ExpressJS React Hello World

This project is intended to be a starting point for a basic Hello World NodeJS ExpressJS and React application
that I repeatedly revisit for many proof of concept projects. The idea is to implement a Todo app, which will
serve as a decent starting point and introduce concepts such as routing, templating, ORM capabilities using SQLite
databases, etc.

The structure of the project is broken into 2 distinct components:

* `client/`: Directory containing the React components.
* `server/`: Directory containing the ExpressJS components (API that the client will interact with).

## Creation of Starter Code

This repository was created using the following starter code:

```bash
# create client
$ npx create-react-app client --view=pug

# create server
$ npx express-generator server --view=pug
$ cd server/
$ npm install --save
```

Following code generation, simply update the port number in `server/bin/www` from `3000` to some other port (e.g. `8000`).
Then you can start the client and server components via the following:

```bash
# client
$ cd client/
$ npm run start

# server
$ cd server/
$ npm run serverstart
```

## Quick Start

If you want to get up and running quickly, simply launch the back-end server, front-end client, and navigate to
[http://localhost:3000](http://localhost:3000) in your browser:

```bash
# server
$ cd server/
$ npm run serverstart

# client
$ cd ../client/
$ npm run start
```

## Server

The following sections detail how to set up some of the server API components, including database and ORM components.

### Models

Models and associated migrations were created and executed using the following (for example) - these steps perform
the following (in order):

* Initialize the database.
* Generate a model and corresponding migration for `Todo`
* Apply the migration to the database (create the `Todo` table and schema)
* Seed the database `Todo` table with a record

```bash
$ ./node_modules/.bin/sequelize init
# then edit config/config.json to your liking

$ npx sequelize-cli model:generate --name todo --attributes text:string,done:boolean
$ npx sequelize-cli db:migrate

$ npx sequelize-cli seed:generate --name first-todo
$ npx sequelize-cli db:seed:all
```

### Starting Server

Start the server in debug mode, after which you can visit [http://localhost:8000/todos](http://localhost:8000/todos)
in your browser:

```bash
$ npm start serverstart
```

You should see a JSON representation of the Todo items in the database.

As a note, the development environment utilizes `nodemon` to manage the services and enables automatic reloads
when local file changes are made (without the need to restart the services each time a file is changed).

### Credit

This tutorial was pieced together with some information from the following sites/resources, among others that were likely missed
in this list:

[Create React Frontend and Node Express Backend...](https://www.freecodecamp.org/news/create-a-react-frontend-a-node-express-backend-and-connect-them-together-c5798926047c/)
[Skeleton Website](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/skeleton_website)
[Sequelize Express](https://sequelize.readthedocs.io/en/1.7.0/articles/express/)
[Sequelize ORM with NodeJS and Express](https://stackabuse.com/using-sequelize-orm-with-nodejs-and-express/)
[Building a Blog...](https://scotch.io/tutorials/build-a-blog-using-expressjs-and-react-in-30-minutes)
[Build a Basic CRUD App...](https://developer.okta.com/blog/2018/07/10/build-a-basic-crud-app-with-node-and-react)
