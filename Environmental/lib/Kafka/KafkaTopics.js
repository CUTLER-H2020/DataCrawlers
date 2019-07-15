'use strict';

const client = require('./KafkaClient.js');

var topics = {
    ANTA_SOC_VISITORS_MONTHLY: {
        topic: "anta_soc_visitors_monthly_draxis",
        partitions: 6,
        replicationFactor: 3
    }
}

var KafkaTopics = {
    client: client,
    topics: topics,
    createAll: (callback = () => {}) => {
        console.info("Creating all topics in Kafka");

        var topicsToCreate = Object.values(topics);

        topicsToCreate.forEach(topic => {
            console.info("Creating " + topic.topic + " (partitions: " + topic.partitions + ", replicationFactor:" + topic.replicationFactor + ")")
        });

        client.createTopics(topicsToCreate, callback);
    }
};

module.exports = KafkaTopics;
