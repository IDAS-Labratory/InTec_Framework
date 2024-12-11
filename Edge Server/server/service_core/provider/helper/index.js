'use strict';
const crypto = require('crypto');
const base64url = require('base64url');

let randomBase64URLBuffer = (len) => {
	len = len || 32;

	let buff = crypto.randomBytes(len);

	return base64url(buff);
};

function randomHex32String() {
	return crypto.randomBytes(32).toString('hex');
}

function hash(data) {
	return crypto.createHash('SHA256').update(data).digest();
}


module.exports = {
	randomBase64URLBuffer,
	randomHex32String,
};
