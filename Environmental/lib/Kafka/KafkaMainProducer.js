'use strict';
const kafka = require('kafka-node'),
  client = new kafka.KafkaClient({
    kafkaHost: '10.10.2.51:9092',
    connectTimeout: 100000
  }),
  producer = new kafka.HighLevelProducer(client),
  EventEmitter = (require('events').EventEmitter.defaultMaxListeners = 0);

const _ = require('lodash');

const chunkNumber = 1000;

module.exports = (msg, topicName) => {
  const broadcastMessageToKafka = (message, i) => {
    let payloads = [
      {
        topic: topicName,
        messages: message
      }
    ];
    return new Promise(resolve => {
      console.log(`Sending ${i} of ${_.chunk(msg, chunkNumber).length}`);
      producer.send(payloads, function(err, data) {
        if (err) return console.log(err);
        resolve(data);
        // resolve(client.close());
      });
    });
  };

  producer
    .on('ready', async function() {
      console.log('Sending...');
      _.chunk(msg, chunkNumber).map(async (m, i) => {
        await broadcastMessageToKafka(m, i);
      });
    })
    .on('error', function(err) {
      console.log(err);
    });
};
