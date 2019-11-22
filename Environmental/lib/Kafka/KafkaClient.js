'use strict';

require('dotenv').config();

const kafka = require('kafka-node');

// create new client
var KafkaClient = new kafka.KafkaClient({
    kafkaHost: '172.16.32.40:9092'
});

// error event
KafkaClient.on('error', function(error) {
    console.error(error);
});

module.exports = KafkaClient;
