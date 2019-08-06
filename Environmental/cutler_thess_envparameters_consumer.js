'use strict';

const es_client = require('./lib/ElasticSearch/Client.js');
const kafka_consumer = require('./lib/Kafka/KafkaConsumer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');
const moment = require('moment');

var topic = kafka_topics.topics.CUTLER_THESS_ENVPARAMETERS.topic;

var consumer = kafka_consumer.create({ topic });

consumer.on('message', function(message) {
  // retrieve item
  var item = JSON.parse(message.value);
  var date = moment(item.date, 'YYYY/MM/DD');

  // insert record in ES
  es_client.index(
    {
      index: topic,
      type: '_doc',
      id: date.format('YYYYMMDD'),
      body: {
        station_name: item.station_name,
        loc: {
          lat: item.loc.lat,
          lon: item.loc.loc
        },
        date: item.date,
        month_: item.month,
        year_: item.year,
        aa: item.aa,
        parameter_name: item.parameter_name,
        parameter_fullname: item.parameter_fullname,
        units: item.units,
        value: item.value,
        daily_aqi: daily_aqi ? daily_aqi : ''
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
