'use strict';

const es_client = require('./lib/ElasticSearch/Client.js');
const kafka_consumer = require('./lib/Kafka/KafkaConsumer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');
const moment = require('moment');

var topic = kafka_topics.topics.CORK_INTEGR_PARKING.topic;

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
        'Parking Option': item['Parking Option'],
        Spaces: item['Spaces'],
        Area: item['Area'],
        'Construction Cost': item['Construction Cost'],
        'Construction Cost per space': item['Construction Cost per space'],
        'Max visitors per day': item['Max visitors per day'],
        'Revenues per space': item['Revenues per space'],
        'Revenues per day': item['Revenues per day'],
        'Revenues - Construction cost': item['Revenues - Construction cost']
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
