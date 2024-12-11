const express = require('express');
const http = require('http');
const https = require('https');
const fs = require('fs');
const bodyParser = require('body-parser');
const cookieSession = require('cookie-session');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const { randomHex32String } = require('../helper');

// Services
//const userService = require('../../services/users/userService');
const monitorService = require('../../services/monitoring/monitorService');

//  SSL certificate and private Key 
const {pk_path , cert_path} = require('../../../config/config')
const privateKey  = fs.readFileSync(pk_path);
const certificate = fs.readFileSync(cert_path);
const credentials = {key: privateKey, cert: certificate};

// Making Express Application
const app = express();

// Parsing request body to JSON
app.use(bodyParser.json())

app.use(cookieSession({
	name: 'seesion',
	keys: [randomHex32String()],
	maxAge: 24*60*60*1000
}));

app.use(cookieParser());

app.use(cors());

// setting response headers
app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Credentials', 'true');
    res.header('Access-Control-Allow-Methods', 'GET,HEAD,PUT,PATCH,POST,DELETE');
    res.header('Access-Control-Expose-Headers', 'Content-Length');
    res.header('Access-Control-Allow-Headers', '*');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    } else {
        return next();
    }
});

// Index page
app.get('/', (req, res, next) => {
    res.status(200).send({msg: "Welcome to Morpho Project (WoT Framework)"});
    next();
});

// Making HTTP and HTTPs server seperately;
var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

// starting services
//userService.start(app);
monitorService.start(app);


module.exports = {
    httpServer,
    httpsServer,
};