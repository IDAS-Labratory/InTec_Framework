const monitorModel = require('../models/monitorModel');
const storageModel = require('../models/storageModel');
 
exports.index = (req,res) => {
    res.status(200).send({
        status: "successed",
        msg: "Monitoring Serivce is OK",
    });
};

exports.storeData = async (req, res) => {
    data = req.body;
    await storageModel.createData(data)
    .then((result) => {
        res.status(201).send({
            status: 201,
            msg: `New data for sensor ${result.device} is recorded successfully!`,
            data_id: result.id
        });
    }).catch(err => {
        console.log("Inserting data has occured an Error: " + err);
        res.status(401).send({
            status: 401,
            Error: `Inserting data has occured an Error:  ${err}!`,     
        });
    });
};

exports.readDataByDevice = (req, res) => {
    let device = req.params.device;
    storageModel.findDataByDeviceId(device) 
    .then((result) => {
        res.status(200).send({
            status: 200,
            msg: `Data for sensor ${device}`,
            data: result
        });
    }).catch(err => {
        console.log("Reading data has occured an Error: " + err);
        res.status(400).send({
            status: 400,
            Error: `Reading data has occured an Error:  ${err}!`,     
        });
    });
};

exports.readStatusDataByDevice = (req, res) => {
    let device = req.params.device;
    storageModel.findStatusDataByDeviceId(device) 
    .then((result) => {
        res.status(200).send({
            status: 200,
            msg: `Data for sensor ${device}`,
            data: result
        });
    }).catch(err => {
        console.log("Reading data has occured an Error: " + err);
        res.status(400).send({
            status: 400,
            Error: `Reading data has occured an Error:  ${err}!`,     
        });
    });
};

exports.dataRecorder = async (data) => {
    await storageModel.recordData(data)
    .catch(err => {
        console.log('An Error occurred: Monitoring Controller could not Setting cache data in database: ' + err)
    });
};