'use strict';

const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

kafka_topics.createAll(function(err, result) {
  if (err) return console.log(err);

  if (result.length == 0) {
    console.log('All topics created successfully!');
  } else {
    console.log('Failed to create the topics!');
    console.error(result);
  }

  kafka_topics.client.close();
});
