const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CORK_ENV_OPW_WL_15MIN.topic;
var messages = [];

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'cork_env_opw_wl_15min_draxis',
    _type: '_doc'
  }
};

var elBody = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/CORK_ENV_OPW_WL_15min.xlsx', {
      sheet_nr: 0,
      ignore_header: 7
    })
    .on('row', function(row) {
      elBody.push(elIndex);
      elBody.push({
        station_name: 'Ringaskiddy NMCI',
        station_location: {
          lat: 51.84,
          lon: 3 - 8.304
        },
        date: moment(row[0]).format('YYYY/MM/DD'),
        date_hour: moment(row[0]).format('YYYY/MM/DD HH:mm'),
        month: moment(row[0]).format('MM'),
        year: moment(row[0]).format('YYYY'),
        hour: moment(row[0]).format('HH:mm'),
        water_level: parseFloat(
          row[1]
            .toLocaleString(undefined, {
              maximumFractionDigits: 3
            })
            .replace(',', '.')
        ),
        unit: 'm'
      });

      messages.push(
        JSON.stringify({
          station_name: 'Ringaskiddy NMCI',
          station_location: {
            lat: 51.84,
            lon: 3 - 8.304
          },
          date: moment(row[0]).format('YYYY/MM/DD'),
          date_hour: moment(row[0]).format('YYYY/MM/DD HH:mm'),
          month: moment(row[0]).format('MM'),
          year: moment(row[0]).format('YYYY'),
          hour: moment(row[0]).format('HH:mm'),
          water_level: parseFloat(
            row[1]
              .toLocaleString(undefined, {
                maximumFractionDigits: 3
              })
              .replace(',', '.')
          ),
          unit: 'm'
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
