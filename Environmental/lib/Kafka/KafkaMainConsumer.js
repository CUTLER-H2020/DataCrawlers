'use strict';
const kafka = require('kafka-node'),
  client = new kafka.KafkaClient({ kafkaHost: '10.10.2.51:9092' }),
  Consumer = kafka.Consumer,
  topics = require('./KafkaTopics'),
  EventEmitter = (require('events').EventEmitter.defaultMaxListeners = 0);

var consumerTopics = [];
Object.values(topics.topics).map(({ topic }, index) => {
  //Check if topic exist, if it doesnt it creates it
  client.loadMetadataForTopics([topic], (err, resp) => {
    if (!resp[1].metadata[topic]) {
      client.createTopics(
        [
          {
            topic: topic
          }
        ],
        (error, result) => {
          console.log(`Topic ${topic} succesfully crated`);
        }
      );
    }
  });
  // End topic existance check

  consumerTopics.push({ topic: topic, partition: 0 });
});

new Consumer(client, consumerTopics)
  .on('message', function(message) {
    console.log(message);
  })
  .on('error', function(err) {
    console.log(err);
  });

console.log('Consumers started...');
