const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CORK_ENV_MET_W_DAILY.topic;
var messages = [];

const metrics = [
  { code: 'date', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'maxtp', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'mintp', description: '', unit: '' },
  { code: 'igmin', description: '', unit: '' },
  { code: 'gmin', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'rain', description: 'Precipitation', unit: 'mm' },
  { code: 'cbl', description: '', unit: '' },
  { code: 'wdsp', description: 'Mean Wind Speed', unit: 'kt' },
  { code: 'ind', description: '', unit: '' },
  { code: 'hm', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  {
    code: 'ddhm',
    description: 'Wind Direction at max 10 min mean',
    unit: 'deg'
  },
  { code: 'ind', description: '', unit: '' },
  { code: 'hg', description: '', unit: '' },
  { code: 'soil', description: 'Temperature', unit: 'C' },
  { code: 'pe', description: '', unit: '' },
  { code: 'evap', description: '', unit: '' },
  { code: 'smd_wd', description: '', unit: '' },
  { code: 'smd_md', description: '', unit: '' },
  { code: 'smd_pd', description: '', unit: '' },
  { code: 'glorad', description: '', unit: '' }
];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/CORK_ENV_MET_W_DAILY.xlsx', {
      sheet_nr: 0,
      ignore_header: 22
    })
    .on('row', function(row) {
      row.map((r, i) => {
        if (i == 8 || i == 17 || i == 10 || i == 14) {
          messages.push(
            JSON.stringify({
              station_name: 'ROCHES POINT',
              station_location: {
                lat: 51.789,
                lon: -8.24
              },
              date: moment(row[0]).format('YYYY/MM/DD'),
              month: moment(row[0]).format('MM'),
              year: moment(row[0]).format('YYYY'),
              parameter: metrics[i].code,
              parameter_description: metrics[i].description,
              parameter_unit: metrics[i].unit,
              parameter_full_name: `${metrics[i].description} (${
                metrics[i].unit
              })`,
              value: parseFloat(r)
            })
          );
        }
      });
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
