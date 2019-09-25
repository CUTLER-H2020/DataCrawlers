'use strict';
const kafka = require('kafka-node'),
  client = new kafka.KafkaClient({ kafkaHost: '10.10.2.51:9092' }),
  producer = new kafka.HighLevelProducer(client);

module.exports = msg => {
  const payloads = [
    {
      topic: 'ANTA_SOC_VISITORS_MONTHLY',
      messages: 'hi'
    }
  ];

  producer
    .on('ready', function() {
      console.log('Sending...');

      producer.send(payloads, function(err, data) {
        if (err) return console.log(err);

        console.log(data);
        client.close();
      });
    })
    .on('error', function(err) {
      console.log(err);
    });
};
