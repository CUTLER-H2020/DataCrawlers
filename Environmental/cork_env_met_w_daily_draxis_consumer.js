'use strict';

const es_client = require('./lib/ElasticSearch/Client.js');
const kafka_consumer = require('./lib/Kafka/KafkaConsumer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');
const moment = require('moment');

var topic = kafka_topics.topics.CORK_ENV_MET_W_DAILY.topic;

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
        station_name: item.station_name,
        station_location: {
          lat: item.station_location.lat,
          lon: item.station_location.lon
        },
        date: item.date,
        month: item.month,
        year: item.year,
        parameter: item.parameter,
        parameter_description: item.parameter_description,
        parameter_unit: item.parameter_unit,
        parameter_full_name: item.parameter_full_name,
        value: item.value
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
