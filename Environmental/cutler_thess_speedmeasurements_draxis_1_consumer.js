'use strict';

const es_client = require('./lib/ElasticSearch/Client.js');
const kafka_consumer = require('./lib/Kafka/KafkaConsumer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');
const moment = require('moment');

var topic = kafka_topics.topics.CUTLER_THESS_SPEEDMEASUREMENTS.topic;

var consumer = kafka_consumer.create({ topic });

consumer.on('message', function(message) {
  // retrieve item
  var item = JSON.parse(message.value);
  var date = moment(item.date, 'YYYY/MM/DD');
  var visitors = item.visitors;

  // insert record in ES
  es_client.index(
    {
      index: topic,
      type: '_doc',
      id: date.format('YYYYMMDD'),
      body: {
        date: item.date,
        day: item.day,
        month: item.month,
        year: item.year,
        time: item.time,
        id: item.id,
        name: item.name,
        speed: item.speed,
        samples: item.samples,
        unit: item.unit,
        // mileage: row[2] * 5,
        mileage_unit: item.mileage_unit
      }
    },
    function(err, resp, status) {
      if (status == 200 || status == 201) {
        console.info('Record ' + resp._id + ' was inserted successfully');
      } else {
        console.log(resp);
      }
    }
  );
});

consumer.on('error', function(error) {
  console.error(error);
});
