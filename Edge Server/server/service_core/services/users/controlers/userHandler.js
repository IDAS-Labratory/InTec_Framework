const userModel = require('../models/userModel');

exports.index = (req,res) => {
    res.status(200).send({
        status: 200,
        msg: "Welcome user!",
    })
};

exports.insertUser = (req, res) => {
    userData = req.body;
    userModel.createUser(userData)
    .then((result) => {
        res.status(201).send({
            status: 201,
            msg: `User ${result.fname} ${result.lname} is created successfully!`,
            user_id: result._id
        });
    }).catch(err => {
        console.log("Inserting user has occured an Error: " + err);
        res.status(401).send({
            status: 401,
            Error: `Inserting user has occured an Error:  ${err}!`,
             
        });
    });    
};

exports.getUserById = (req, res) => {
    userId =req.params.userId;
    userModel.findUserById(userId)
    .then( (result) => {
        res.status(200).send({
            status: 200,
            msg: `User is ${result.email}!`,
            user: result
        });
    }).catch(err => {
        console.log("Getting user by id is occured Error: " + err);
        res.status(400).send({
            status: 400,
            msg: ` User ID:${userId} dose not match`,
            Error: `Getting user by id is occured Error:  ${err}!`,
             
        });
    });
};
