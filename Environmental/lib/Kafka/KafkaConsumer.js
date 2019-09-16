'use strict';

require('dotenv').config();

const kafka = require('kafka-node');

var KafkaConsumer = {
    create: ({topic, group_id = null}) => {
        if (!group_id) {
            group_id = "g1"
        }

        // create a consumer group
        var options = {
            kafkaHost: process.env.KAFKA_HOST,
            groupId: group_id,
            protocol: ['roundrobin']
        };

        var consumer = new kafka.ConsumerGroup(options, topic);

        console.info('Started consumer for topic "' + topic + '" in group "' + group_id + '"');

        return consumer;
    }
};

module.exports = KafkaConsumer;
