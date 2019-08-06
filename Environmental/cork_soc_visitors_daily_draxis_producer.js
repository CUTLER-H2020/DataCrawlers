const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CORK_SOC_VISITORS_DAILY.topic;
var messages = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/visitor_numbers_cork.xlsx', {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      messages.push(
        JSON.stringify({
          date: moment(row[0]).format('YYYY/MM/DD'),
          month: moment(row[0]).format('MM'),
          year: moment(row[0]).format('YYYY'),
          visitors: row[1],
          pay_visitors: row[2],
          ticket_price: 5,
          ticker_unit: 'euro',
          incomes: row[2] * 5
        })
      );
    })
    .on('end', function(err) {
      kafka_producer.send({ topic, messages }, function(err, data) {
        if (!err) {
          console.log('All messages succesfully sent!');
        } else {
          console.log('Failed to send the messages!');
          console.log(err);
        }

        kafka_producer.client.close();
      });
    });
})();
