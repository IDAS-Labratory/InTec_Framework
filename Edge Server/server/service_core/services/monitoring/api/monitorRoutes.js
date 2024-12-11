const express = require('express');
const handler = require('../controllers/monitorHandler');

var router = express.Router();

router.use((req, res, next) => {
    console.log("< Monitoring service is called! >");
    next();
});

router.route('/').get((req, res) => {
    handler.index(req, res);
});

router.route('/record').post((req, res) => {
    handler.storeData(req, res);
});

router.route('/:device').get((req, res) => {
    handler.readDataByDevice(req, res);
});

router.route('/status/:device/').get((req, res) => {
    handler.readStatusDataByDevice(req, res);
});

/* 
router.route('/getvalue/:id').get((req, res) => {
    handler.valueCacheGetter(req, res).catch(err => {
        console.log("An Error occurred in Monitoring Router, /getvalue: "+ err);
    });    
})
*/
module.exports = router;