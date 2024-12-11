// MQTT Broker Server
const mosca = require('mosca');
const config = require('../../../config/config');
var mqttServer;


function selectBackend(backend) {
    switch (backend){
        default:
            return {
                type: 'mongo',
                url: config.mqtt_backend_url,
                pubsubCollection: 'ascoltatori',
                mongo: {}
            }

        case 'mongodb' || 'mongo' || 'MongoDB':
            return {
                type: 'mongo',
                url: config.mqtt_backend_url,
                pubsubCollection: 'ascoltatori',
                mongo: {}
            }

        case 'redis':
            return {
                type: 'redis',
                redis: require('redis'),
                db: 12,
                port: 6379,
                return_buffers: true, // to handle binary payloads
                host: config.host_ip
            }

        case 'none':
            return {}
    }
}

exports.start = () => {
    // Config MQTT server
    var Setting = {
        port: Number(config.mqtt_port),
        backend: selectBackend(config.mqtt_backend)
    };
    // Create MQTT server
    mqttServer = new mosca.Server(Setting)

    mqttServer.on("ready", () =>{
        console.log("> MQTT broker server is Running on port: " + Setting.port)
    });

    mqttServer.on('clientConnected', function(client) {
        console.log(`>> client ${client.id} connected to MQTT server`);
    });
};