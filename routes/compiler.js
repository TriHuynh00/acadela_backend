var express = require('express');
var router = express.Router();
const compilerController = require("../controller/compiler/compiler");

/* GET home page. */
router.post('/', compilerController.compile);

module.exports = router;
