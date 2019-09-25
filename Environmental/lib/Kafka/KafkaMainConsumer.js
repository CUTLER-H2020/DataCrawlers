'use strict';
const kafka = require('kafka-node'),
  client = new kafka.KafkaClient({ kafkaHost: '10.10.2.51:9092' }),
  Consumer = kafka.Consumer,
  topics = require('./KafkaTopics'),
  EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.setMaxListeners(100000);

Object.values(topics.topics).map(async ({ topic }, index) => {
  //Check if topic exist, if it doesnt it creates it
  await client.loadMetadataForTopics([topic], async (err, resp) => {
    if (!resp[1].metadata[topic]) {
      client.createTopics(
        [
          {
            topic: topic,
            partitions: 1,
            replicationFactor: 2
          }
        ],
        (error, result) => {
          console.log(`Topic ${topic} succesfully crated`);
        }
      );
    }
  });
  //End topic existance check

  //Initialise Consumer
  new Consumer(client, [{ topic: topic, partition: 0 }])
    .on('message', function(message) {
      console.log(message);
    })
    .on('error', function(err) {
      console.log(err);
    });
  //End of initiliasation
});

console.log('Consumers started...');
