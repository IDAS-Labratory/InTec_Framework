const {redis_url} = require('../../../../config/config');
const engine = require('../../../database/engine');
var redis;
//redis = engine.createDB({db: "redis", url: redis_url});
//const pipeline = redis.pipeline();

exports.valueSetter = async (data) => {
    redis.set(data.id, JSON.stringify(data));
};

exports.valueGetter = async (data) => {
    result = await redis.get(String(data)); 
    if(!result)
        throw "Device is not exist!";
        
    jsonResult = JSON.parse(result);
    return jsonResult;
};