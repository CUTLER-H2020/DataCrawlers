require('dotenv').config({path: __dirname + '/../../.env'});

const KAFKA_HOST = process.env.KAFKA_HOST;
const KAFKA_PORT = process.env.KAFKA_PORT;

const KAFKA_CA_FILE = process.env.KAFKA_CA_FILE;
const KAFKA_CERT_FILE = process.env.KAFKA_CERT_FILE;
const KAFKA_KEY_FILE = process.env.KAFKA_KEY_FILE;

const ES_HOST = process.env.ES_HOST;
const ES_PORT = process.env.ES_PORT;
const ES_USER = process.env.ES_USER;
const ES_PASSWORD = process.env.ES_PASSWORD;
const ES_CA_CERTS = process.env.ES_CA_CERTS;


module.exports = {
    KAFKA_HOST,
    KAFKA_PORT,
    KAFKA_CA_FILE,
    KAFKA_CERT_FILE,
    KAFKA_KEY_FILE,
    ES_HOST,
    ES_PORT,
    ES_USER,
    ES_PASSWORD,
    ES_CA_CERTS
}