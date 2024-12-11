const {http, http_port, https_port, host_ip } = require('../config/config');
const {httpServer, httpsServer} = require('./provider/server/http');
const mqttServer = require('./provider/server/mqtt');

// Starting HTTP server if HTTP Config set true in configFile.
if (Boolean(http) == true)
    startHTTP(httpServer ,http_port, host_ip);

// Starting HTTPS server.
startHTTPS(httpsServer ,https_port, host_ip);

//Starting MQTT Server
//mqttServer.start();

function startHTTP(httpServer ,http_port, host_ip){
    httpServer.listen(http_port, host_ip, () => {
        console.log("> HTTP server is Running on port: " + http_port)
        console.log("> Open the server on local host: http://"+host_ip+ ":" + http_port);
});
};

function startHTTPS(httpsServer ,https_port, host_ip){
    httpsServer.listen(https_port, host_ip, () => {
        console.log("> HTTPS server is Running on port: " + https_port)
        console.log("> Open the server on local host: https://"+host_ip+ ":" + https_port);
});
};