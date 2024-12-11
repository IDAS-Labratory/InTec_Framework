const {db_url, database} = require('../../../../config/config')
const engine = require('../../../database/engine')
var mongoose;
mongoose = engine.createDB({db: database, url: db_url});

var userSchema = mongoose.Schema({
    id: {
        type: String,
    },
    name: {
        type: String,
        unique: false
    },
    email: {
        type: String,
    },
    authenticators: {
        type: Array,
    },
    registered: {
        type: Boolean,
        default: false,
    },
});

const User = mongoose.model('Users', userSchema);


exports.createUser = (newUserData) => {
    const user = new User(newUserData);
    user.save();
    return user;
};

exports.findUserById = (id) => {
    return User.findById(id)
        .then((result) => {
            result = result.toJSON();
            delete result._id;
            delete result.__v;
            return result;
        });
};

exports.findUserByEmail = async (email) => {
    result = await User.findOne({'email': email});
    return result;
};

exports.patchUser = (id, userData) => {
    return User.findOneAndUpdate({
        _id: id
    }, userData);
};

exports.removeByEmail = async (email) => {
    result = await User.findOneAndRemove({ 'email': email });
    return result;
    
};

exports.removeById = (userId) => {
    return new Promise((resolve, reject) => {
        User.deleteMany({_id: userId}, (err) => {
            if (err) {
                reject(err);
            } else {
                resolve(err);
            }
        });
    });
};
