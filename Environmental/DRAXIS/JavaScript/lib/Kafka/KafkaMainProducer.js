'use strict';
// const kafka = require('kafka-node');
// const client = new kafka.KafkaClient({
//   kafkaHost: '172.16.32.40:9092',
//   connectTimeout: 100000,
//   requestTimeout: 2147483647
// });
// const producer = new kafka.HighLevelProducer(client);
// const EventEmitter = (require('events').EventEmitter.defaultMaxListeners = 0);

const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['172.16.32.30:9092']
});
const producer = kafka.producer();

const _ = require('lodash');

const KafkaTopics = require('./KafkaTopics');

const chunkNumber = 1000;
var count = 0;
var sendCount = 0;
module.exports = (msg, topicName) => {
  const broadcastMessageToKafka = (message, i) => {
    producer
      .send({
        topic: topicName,
        messages: message.map(mes => {
          return { value: JSON.stringify(mes) };
        })
      })
      .then(res => {
        sendCount += message.length;
        console.log(
          `Broadcasted ${message.length} in count ${sendCount} of ${count} messages`
        );
      })
      .catch(err => console.log(err));

    count += message.length;
  };

  // _.chunk(msg, chunkNumber).map(async (m, i) => {
  //   return broadcastMessageToKafka(m, i);
  // });

  // Promise.all(
  //   _.chunk(msg, chunkNumber).map(async (m, i) => {
  //     return await broadcastMessageToKafka(m, i);
  //   })
  // );

  // producer
  //   .on('ready', async function() {
  console.log('Sending... Before');
  producer
    .connect()
    .then(res => {
      console.log('Producer Connected');
      Promise.all(
        _.chunk(msg, chunkNumber).map(async (m, i) => {
          return await broadcastMessageToKafka(m, i);
        })
      );
    })
    .catch(err => console.log(err));
  console.log('Succesfully Broadcast All messages!');
  console.log('Broadcasting to finish!');
  console.log(`Broadcasted ${count} messages`);

  producer.send(
    [
      {
        topic: KafkaTopics.topics[topicName].finish,
        messages: [
          {
            msg: 'finish'
          }
        ]
      }
    ],
    function(err, data) {
      if (err) return console.log(err);
      console.log(data);
      console.log('Message broadcasted to Finish topic. Client will close.');

      // client.close();
    }
  );
};
