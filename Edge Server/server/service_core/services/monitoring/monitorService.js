const monitorRoutes = require('./api/monitorRoutes');
const deviceListenner = require('./listeners/mqttListenner');

exports.start = (app) => {
    //deviceListenner.start('prediction');
    app.use('/monitor', monitorRoutes);
    console.log("> Monitoring service is started successfully!");
};
