var express = require('express');
var router = express.Router();
const compilerController = require("../controller/compiler");

/* GET home page. */
router.get('/', compilerController.compile);

module.exports = router;
