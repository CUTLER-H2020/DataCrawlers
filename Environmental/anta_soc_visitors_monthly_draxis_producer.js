'use strict';

const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.ANTA_SOC_VISITORS_MONTHLY.topic;
const xlsx_file = __dirname + '/visitor_numbers.xlsx';

var messages = [];

const extractValues = (async () => {
  console.log('Opening file "' + xlsx_file + '"');

  new XLSX()
    .extract(xlsx_file, {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      // ignore if we don't have a value for "date" or "visitors"
      if (!row[0] || !row[1]) {
        return;
      }

      // construct message
      var message = {
        date: moment(row[0]).format('YYYY/MM/DD'),
        month: moment(row[0]).format('MM'),
        year: moment(row[0]).format('YYYY'),
        visitors: parseInt(row[1])
      };

      console.log('Reading row - date: ' + message.date + ' | visitors: ' + message.visitors);
      
      // push row values as "message"
      messages.push(JSON.stringify(message));
    })
    .on('end', function(err) {
      kafka_producer.send({topic, messages}, function (err, data) {
        if (!err) {
            console.log('All messages succesfully sent!');
        } else {
            console.log('Failed to send the messages!');
            console.log(err)
        }
    
        kafka_producer.client.close();
      });
    });
})();
