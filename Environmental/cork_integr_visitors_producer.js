const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
const data = require('./files/cork_max_visitors_revenues_yearly');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CORK_INTEGR_VISITORS.topic;
var messages = [];

var elIndex = {
  index: {
    _index: 'cork_integr_visitors',
    _type: '_doc'
  }
};

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elBody = [];

const saveToElastic = async elBody => {
  return await kafka_producer.send({ topic, messages }, function(err, data) {
    if (!err) {
      console.log('All messages succesfully sent!');
    } else {
      console.log('Failed to send the messages!');
      console.log(err);
    }

    kafka_producer.client.close();
  });
};

const extractValues = (async () => {
  data.map((d, i) => {
    if (i % 2 !== 0) {
      var returnVal = {
        date: moment(d['Date']).format('YYYY/MM/DD'),
        'No of Visitors': d['No of Visitors'],
        Revenues: d['Revenues']
      };
      if (returnVal) {
        elBody.push(elIndex);
        elBody.push(returnVal);
        messages.push(JSON.stringify(returnVal));
      }
    }
  });

  if (elBody.length) saveToElastic(elBody);
})();
