const { v4: uuidv4 } = require('uuid');
const {db_url, database, collection_name} = require('../../../../config/config')
const engine = require('../../../database/engine')
var mongoose;
mongoose = engine.createDB({db: database, url: db_url});

var sensorSchema = mongoose.Schema({
     id: {
          type: String,
          default: uuidv4(),
     },
     device: {
          type: String,
          unique: false
     },
     date: {
          type: Date,
     },
     windowSize: {
          type: Number,
     },
     label: {
          type: Number,
     },
     latency:{
          type: Number
     },
     data: {
           type: Object,
     },
});

const Sensor = mongoose.model(collection_name, sensorSchema);

exports.recordData = async (data) => {
     const sensor = new Sensor(data);
     sensor.save();
     return sensor;
 };

exports.findDataByDeviceId = (id) => {
     return Sensor.find({'device' : id})
         .then((result) => {
             return result;
         });
 };

 exports.findStatusDataByDeviceId = (id) => {
     return Sensor.findOne({'device' : id}, 'id label latency date').sort({date: -1})
         .then((result) => {
             return result;
         });
 };
