const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');
const stations = require('./files/stations');

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.RAIN_1.topic;
var messages = [];

const createIndex = async () => {
  await client.indices.create({
    index: 'rain_1',
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
  });
};

const saveToElastic = async (index, elBody) => {
  return await client.bulk(
    {
      requestTimeout: 600000,
      body: elBody
    },
    function(err, resp) {
      if (err) console.log(err.response);
      else console.log(index + ' succesfully indexed!');
    }
  );
};

createIndex();

const extractValues = (async () => {
  let index = 0;
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/alladata_v20_deel2.xlsx', {
      sheet_nr: 8,
      ignore_header: 1
    })
    .on('row', async row => {
      row.map(async (col, i) => {
        if (i > 0 && i % 2 == 0 && col != undefined) {
          var returnVal = {
            code: stations[i].code,
            station_name: stations[i].name,
            station_location: {
              lat: stations[i].loc.lat,
              lon: stations[i].loc.lon
            },
            date: moment(row[0]).format('YYYY/MM/DD HH:mm:ss'),
            measurement: col
          };

          if (returnVal) {
            messages.push(JSON.stringify(returnVal));
          }
        }
      });

      if (index > 0 && index % 50000 == 0 && elBody.length) {
        console.log('Indexing ' + index);
        saveToElastic(index, elBody);
        elBody = [];
      }
      index++;
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
