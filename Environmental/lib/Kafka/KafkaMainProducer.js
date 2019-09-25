'use strict';
const kafka = require('kafka-node'),
  client = new kafka.KafkaClient({ kafkaHost: '10.10.2.51:9092' }),
  producer = new kafka.HighLevelProducer(client);

module.exports = msg => {
  const payloads = [
    {
      topic: 'ANTA_SOC_VISITORS_FINISH_MONTHLY',
      messages: 'hi',
      partition: 0
    }
  ];
  producer
    .on('ready', function() {
      console.log('sending');

      producer.send(payloads, function(err, data) {
        console.log(data);
        client.close();
      });
    })
    .on('error', function(err) {
      console.log(err);
    });
};
