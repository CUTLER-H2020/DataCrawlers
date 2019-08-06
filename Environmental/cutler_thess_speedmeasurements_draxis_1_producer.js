// const XLSX = require('xlsx-extract').XLSX;
const XLSX = require('xlsx');

const moment = require('moment');
var fs = require('fs');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CUTLER_THESS_SPEEDMEASUREMENTS.topic;

client.indices.create(
  {
    index: 'cork_soc_visitors_daily_draxis',
    body: {
      settings: {
        number_of_shards: 1
      },
      mappings: {
        _doc: {
          properties: {
            station_location: {
              type: 'geo_point'
            }
          }
        }
      }
    }
  },
  (err, resp) => {
    // if (err) console.log(err);
    console.log('Index Created Succesfully');
  }
);

fs.readdir(__dirname + '/files', function(err, files) {
  if (err) {
    console.error('Could not list the directory.', err);
    process.exit(1);
  }

  files.map(file => {
    console.log('Opening file: ' + file);

    var workbook = XLSX.readFile(__dirname + '/files/' + file, {
      type: 'binary',
      cellDates: true,
      cellStyles: true
    });

    workbook.SheetNames.map(sheet => {
      // console.log(workbook.Sheets[sheet]);
      var xlData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet]);
      var messages = [];
      xlData.map(row => {
        messages.push(
          JSON.stringify({
            date: moment(row.Timestamp).format('YYYY/MM/DD HH:mm'),
            day: moment(row.Timestamp).format('DD'),
            month: moment(row.Timestamp).format('MM'),
            year: moment(row.Timestamp).format('YYYY'),
            time: moment(row.Timestamp).format('HH:mm'),
            id: row.PathID,
            name: row.Name ? row.Name.split('. ')[1] : '',
            speed: row.Value,
            samples: row.Samples,
            unit: 'u (km/h)',
            // mileage: row[2] * 5,
            mileage_unit: 'vkm (km*cars)'
          })
        );
      });
    });

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
});
