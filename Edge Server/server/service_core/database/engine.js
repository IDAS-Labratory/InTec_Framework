const mongo_db = require('./dbs/mongoDB');
const redis_db = require('./dbs/redisDB');
var database;

exports.createDB = (config) => {
    switch(config.db){
        case "MongoDB" || "mongo" || "Mongo":
            database = mongo_db.start(config.url);
            break;
        case "redis" || "RedisDB" || "Redis":
            database = redis_db.start(config.url);
            break;
    };
    
    return database;
};