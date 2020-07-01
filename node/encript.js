'use strict';

var CryptoJS = require('crypto-js');
var util = require('util');
/**
 * Epayco constructor
 *
 * @param {Object} options
 * @return {Epayco} API client instance
 * @api public
 */

function Epayco(options) {
    if (!(this instanceof Epayco)) {
        return new Epayco(options);
    }

    if (
        'string' != typeof options.apiKey ||
        'string' != typeof options.privateKey ||
        'string' != typeof options.lang ||
        'boolean' != typeof options.test
    ) {
        console.log('error');
    }

    /**
     * Init settings
     */
    this.apiKey = options.apiKey;
    this.privateKey = options.privateKey;
    this.lang = options.lang;
    this.test = options.test ? 'TRUE' : 'FALSE';
    this.encript = new encript(this);
}

function encript(epayco) {
    Resource.call(this, epayco);
}

util.inherits(encript, Resource);

/**
 * Create Subscriptions
 * @param {Object} options
 * @api public
 */
encript.prototype.create = function(options) {
    return this.request(options);
};

/**
 * Resource constructor
 *
 * @param {Epayco} epayco
 */

function Resource(epayco) {
    this._epayco = epayco;
}

Resource.prototype.request =async function(data)  {
    var dataEncripted;
    dataEncripted =await setData(data, this._epayco.privateKey, this._epayco.apiKey, this._epayco.test);
    return  JSON.stringify(dataEncripted);
}

function setData(data, privateKey, publicKey, test) {
  
    var set = {},
    hex = encryptHex(privateKey);
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            set[langkey(key)] = encrypt(data[key], privateKey);
        }
    }
    set["public_key"] = publicKey;
    set["i"] = hex.i;
    set["enpruebas"] = encrypt(test, privateKey);
    set["lenguaje"] = "javascript";
    set["p"] = hex.p;

    return set;
}

/**
 * Get bites petition secure
 * @param  {string} userKey private key user
 * @return {object}         bites from crypto-js
 */
function encryptHex(userKey) {
    var key = CryptoJS.enc.Hex.parse(userKey),
        iv = CryptoJS.enc.Hex.parse("0000000000000000");
    return {
        i: iv.toString(CryptoJS.enc.Base64),
        p: key.toString(CryptoJS.enc.Base64)
    }
}

/**
 * Traslate keys
 * @param  {string} value key eng
 * @return {string}       traslate key
 */
function langkey(value) {
	var obj = require("./keylang.json");
	if (obj[value]) {
		return obj[value]
	} else {
		return value
	}
}

/**
 * Encrypt text
 * @param  {string} value plain text
 * @param  {string} key   private key user
 * @return {string}       text encrypt
 */
function encrypt(value, userKey) {
    var key = CryptoJS.enc.Hex.parse(userKey),
        iv = CryptoJS.enc.Hex.parse("0000000000000000"),
        text = CryptoJS.AES.encrypt(value, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
    return text.ciphertext.toString(CryptoJS.enc.Base64);
}



var epayco = Epayco({
    apiKey: 'c84ad754c728bfb10af2c1c3d1594106',
    privateKey: '448897b08db8a1ae6e72441fb6101a8b',
    lang: 'ES',
    test: false
})

var pse_info = {
    bank: "1007",
    invoice: "1472050778p1",
    description: "pay test",
    value: "20000",
    tax: "0",
    tax_base: "20000",
    currency: "COP",
    type_person: "0",
    doc_type: "CC",
    doc_number: "10358519",
    name: "testing",
    last_name: "PAYCO",
    email: "no-responder@payco.co",
    country: "CO",
    cell_phone: "3010000001",
    ip:"190.000.000.000", /*This is the client's IP, it is required */
    url_response: "https://ejemplo.com/respuesta.html",
    url_confirmation: "https://ejemplo.com/confirmacion",
    method_confirmation: "GET"

}
epayco.encript.create(pse_info)
    .then(function(bank) {
        console.log(bank);
    })
    .catch(function(err) {
        console.log("err: " + err);
});