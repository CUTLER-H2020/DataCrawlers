'use strict';
const { Client } = require('@elastic/elasticsearch');
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'cutler',
  brokers: ['10.10.2.51:9092']
});

const topics = require('./KafkaTopics');

const consumer = kafka.consumer({ groupId: 'kaf-pis' });

consumer.connect();

// const kafka = require('kafka-node'),
//   client = new kafka.KafkaClient({
//     kafkaHost: '10.10.2.51:9092',
//     connectTimeout: 100000,
//     requestTimeout: 2147483647
//   }),
//   Consumer = kafka.Consumer,
//   topics = require('./KafkaTopics'),
//   EventEmitter = (require('events').EventEmitter.defaultMaxListeners = 0),
const elasticSearchclient = new Client({
  node: 'http://10.10.2.56:9200'
});

var consumerTopics = [];
Object.values(topics.topics).map(async ({ topic }, index) => {
  //Check if topic exist, if it doesnt it creates it
  // client.loadMetadataForTopics([topic], (err, resp) => {
  //   if (!resp[1].metadata[topic]) {
  //     client.createTopics(
  //       [
  //         {
  //           topic: topic
  //         }
  //       ],
  //       (error, result) => {
  //         if (error) return console.log(error);

  //         console.log(`Topic ${topic} succesfully crated`);
  //       }
  //     );
  //   }
  // });
  // End topic existance check
  await consumer.subscribe({ topic: topic });
  consumerTopics.push({ topic: topic, partition: 0 });
});
var count = 1;
var countLength = 0;

consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    if (topics.topics[topic].finish) {
      var item = JSON.parse(message.value.toString());
      // console.log({
      //   count: count
      // });
      // count++;
      elasticSearchclient
        .index({
          index: topics.topics[topic].index,
          type: '_doc',
          body: item
        })
        .then(res => {
          console.log({
            count: count
          });
          count++;
        })
        .catch(err => {});
    }
  }
});

// new Consumer(client, consumerTopics)
//   .on('message', function(msg) {
//     // console.log(topics);

//     // count++;
//     if (topics.topics[msg.topic].finish) {
//       var item = JSON.parse(msg.value);

//       elasticSearchclient
//         .index({
//           index: topics.topics[msg.topic].index,
//           type: '_doc',
//           body: item
//         })
//         .then(res => {
//           console.log({
//             count: count
//             // index: topics.topics[msg.topic]
//           });
//           count++;
//         })
//         .catch(err => {});
//     }
//   })
//   .on('error', function(err) {
//     console.log(err);
//   });

console.log('Consumers started...');
