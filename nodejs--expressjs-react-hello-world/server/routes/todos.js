var express = require('express');
var router = express.Router();

// controllers
const todoController = require('../controllers').todo;

/* GET todos listing. */
router.get('/', todoController.list);

module.exports = router;
