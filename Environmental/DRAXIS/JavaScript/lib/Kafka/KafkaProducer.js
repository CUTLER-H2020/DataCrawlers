'use strict';

const kafka = require('kafka-node');

const client = require('./KafkaClient.js');

// create a producer
var producer = new kafka.HighLevelProducer(client);

// ready event
var ready = false;
producer.on("ready", function() {
    ready = true;
    
    //console.log("Kafka Producer is connected and ready.");
});

// error event
producer.on("error", function(error) {
    console.error(error);
});

var KafkaProducer = {
    client: client,
    send: ({ topic, messages }, callback = () => {}) => {
        // check if producer is ready...
        if (!ready) {
            setTimeout(function() {
                KafkaProducer.send({topic, messages}, callback);
            }, 500);

            return;
        }

        console.log("Sending messages to topic " + topic);

        // build the payload
        var payloads = [];

        messages.forEach(message => {
            payloads.push({
                "topic": topic,
                "messages": message
            })    
        });

        // send the messages
        producer.send(payloads, callback);
    }
};

module.exports = KafkaProducer;
