const mongoose = require('mongoose');
let count = 0;

const options = {
    autoIndex: false, // Don't build indexes
    poolSize: 10, // Maintain up to 10 socket connections
    // If not connected, return errors immediately rather than waiting for reconnect
    bufferMaxEntries: 0,
    // all other approaches are now deprecated by MongoDB:
    useNewUrlParser: true,
    useUnifiedTopology: true,
    // Using findOneAndUpdate() and findOneAndDelete() without the `useFindAndModify` option set to false are deprecated.
    useFindAndModify: false
};

exports.start = (db_url) => { 
    const connectWithRetry = () => {
    console.log('> MongoDB connection with retry...')
    mongoose.connect(db_url, options).then(()=>{
        console.log('> MongoDB is connected successfully!')
        }).catch(err=>{
        console.log('> MongoDB connection unsuccessful, retry after 5 seconds. ', ++count);
        setTimeout(connectWithRetry, 5000)
        })
    };
    connectWithRetry();
    return mongoose;
};