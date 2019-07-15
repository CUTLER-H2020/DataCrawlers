'use strict';

require('dotenv').config();

const kafka = require('kafka-node');

// create new client
var KafkaClient = new kafka.KafkaClient({
    kafkaHost: process.env.KAFKA_HOST
});

// error event
KafkaClient.on('error', function(error) {
    console.error(error);
});

module.exports = KafkaClient;
