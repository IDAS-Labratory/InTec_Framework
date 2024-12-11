//const userHandler = require('./handlers/userHandler');
const userRoutes = require('./api/userRoutes')

exports.start = (app) => {
    app.use('/users', userRoutes);
    console.log("> User service is started successfully!");
};
