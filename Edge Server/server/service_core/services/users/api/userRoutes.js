const express = require('express');
const handler = require('../controlers/userHandler');
var router = express.Router();


router.use((req, res, next) => {
    console.log("< User service is called! >");
    next();
});

router.route('/').get((req, res) => {
    handler.index(req, res);
});

router.route('/insert').post( (req,res) => { 
    handler.insertUser(req,res);
});

router.route('/get/:userId').get( (req, res) => {  
    handler.getUserById(req, res)
});

module.exports = router;