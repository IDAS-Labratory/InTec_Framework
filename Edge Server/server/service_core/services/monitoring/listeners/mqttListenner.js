//subscriber.js
const mqtt = require('mqtt');
const monitorHandler = require('../controllers/monitorHandler');
const {mqtt_broker} = require('../../../../config/config');

const mqttURL = 'mqtt://' + mqtt_broker;
const client  = mqtt.connect(mqttURL);
client.setMaxListeners(100);


exports.start = (top) => {
    client.on('connect', function () {
        client.subscribe(top);
        console.log('> Device Service is listenning on Topic: '+ top);
    });
    client.on('message', function (topic, message) {
        
        let jsonMessage = JSON.parse(message);

        console.log(">> Subscriber on topic: "+ topic + ", Date is: " + jsonMessage.date + ", Message Label is: " + jsonMessage.label);
        monitorHandler.dataRecorder(jsonMessage)
        .catch(err => {
            console.log(`An Error occurred on Device Listenner topic ${topic}. could not patching data in database: ` + err)
        });
    });
};