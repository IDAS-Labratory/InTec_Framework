const Redis = require('ioredis');
let count = 0;

exports.start = (db_url) => { 
    const connectWithRetry = () => {
        console.log('> Redis connection with retry...');
        try {
            const redis = new Redis(db_url);
            console.log('> Redis is connected successfully!');
            return redis;
        } catch (error) {
            console.log('> Redis connection unsuccessful, retry after 5 seconds. ', ++count);
            setTimeout(connectWithRetry, 5000);
        }
    };
    let redis = connectWithRetry();
    return redis;
};