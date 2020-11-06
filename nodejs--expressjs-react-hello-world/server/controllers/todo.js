const Todo = require('../models').todo;

module.exports = {
  list(req, res) {
    return Todo
      .findAll({
        order: [
          ['createdAt', 'DESC'],
        ],
      })
      .then((todos) => res.status(200).send(todos))
      .catch((error) => { res.status(400).send(error); });
    },

  /* BOILERPLATE CODE - UPDATE AS NECESSARY/NEEDED
  getById(req, res) {
    return Todo
      .findByPk(req.params.id, {
        include: [{
            model: Todo,
            as: 'todos'
        }],
      })
      .then((todo) => {
        if (!todo) {
          return res.status(404).send({
            message: 'Todo Not Found',
          });
        }
        return res.status(200).send(todo);
      })
      .catch((error) => {
        console.log(error);
        res.status(400).send(error);
      });
  },

  add(req, res) {
    return Todo
      .create({
        todo_text: req.body.todo_text,
      })
      .then((todo) => res.status(201).send(todo))
      .catch((error) => res.status(400).send(error));
  },

  update(req, res) {
    return Todo
      .findByPk(req.params.id, {
        include: [{
          model: Todo,
          as: 'todos'
        }],
      })
      .then(todo => {
        if (!todo) {
          return res.status(404).send({
            message: 'Todo Not Found',
          });
        }
        return todo
      .update({
        todo_text: req.body.todo_text || todo.text,
      })
      .then(() => res.status(200).send(todo))
      .catch((error) => res.status(400).send(error));
    })
    .catch((error) => res.status(400).send(error));
  },

  delete(req, res) {
    return Todo
      .findByPk(req.params.id)
      .then(todo => {
        if (!todo) {
          return res.status(400).send({
            message: 'Todo Not Found',
          });
        }
        return todo
      .destroy()
      .then(() => res.status(204).send())
      .catch((error) => res.status(400).send(error));
    })
    .catch((error) => res.status(400).send(error));
  },
  */
};
