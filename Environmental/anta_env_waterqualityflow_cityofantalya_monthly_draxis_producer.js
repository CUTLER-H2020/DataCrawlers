const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic =
  kafka_topics.topics.ANTA_ENV_WATERQUALITYFLOW_CITYOFANTALYA_MONTHLY.topic;
var messages = [];

const units = [
  { pollutant: 'BOD', unit: 'mg/L', DL: 5 },
  { pollutant: 'Dissolved Oxygen', unit: 'mg/L' },
  { pollutant: 'Fecal coliform', unit: 'CFU/100mL' },
  { pollutant: 'Fecal Streptococcus', unit: 'CFU/100mL' },
  { pollutant: 'COD', unit: 'mg/L', DL: 5 },
  { pollutant: 'pH' },
  { pollutant: 'Total Nitrogen', unit: 'mg/L', DL: 1.32 },
  { pollutant: 'Total Coliform', unit: 'CFU/100mL' },
  { pollutant: 'Total Phosphorus', unit: 'mg/L', DL: 0.025 },
  { pollutant: 'Depth', unit: 'm3/sec' },
  { pollutant: 'Flow', unit: 'm/sec' }
];

var elBody = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/anta_water_quality_flow_2018_2019.xlsx', {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      row.map((r, i) => {
        if (i > 3) {
          if (r) r = r.toString().indexOf('<') > -1 ? units[i - 4].DL : r;

          messages.push(
            JSON.stringify({
              station_name: row[1],
              station_location: {
                lat: row[2],
                lon: row[3]
              },
              date: moment(row[0]).format('YYYY/MM/DD'),
              month: moment(row[0]).format('MM'),
              year: moment(row[0]).format('YYYY'),
              day: moment(row[0]).format('DD'),
              parameter_name: units[i - 4].pollutant,
              parameter_fullname: `${units[i - 4].pollutant} ${
                units[i - 4].unit
              }`,
              unit: units[i - 4].unit,
              value: r
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
