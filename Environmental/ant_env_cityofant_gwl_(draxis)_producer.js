const XLSX = require('xlsx-extract').XLSX;
const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.ANT_ENV_CITYOFANT_GWL.topic;
var messages = [];
var stations = [];

const extractStations = () => {
  let data = [];
  return new Promise((resolve, reject) => {
    new XLSX()
      .extract(__dirname + '/Export_CUTLER_v40.xlsx', {
        sheet_nr: 0,
        ignore_header: 1
      })
      .on('row', function(row) {
        data.push(row);
      })
      .on('end', function(err) {
        resolve(data);
      });
  });
};

const extractValues = (async () => {
  console.log('Indexing Stations');
  stations = await extractStations();

  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/Export_CUTLER_v40.xlsx', {
      sheet_nr: 3,
      ignore_header: 1
    })
    .on('row', function(row) {
      let selectedStation = stations.filter(station => {
        return station[0] == row[0];
      })[0];
      if (selectedStation && row[2] != undefined) {
        messages.push(
          JSON.stringify({
            station_id: selectedStation[0].toString(),
            station_name: selectedStation[9].toString(),
            station_location: {
              lat: selectedStation[11],
              lon: selectedStation[10]
            },
            date: row[1],
            peil_cor: row[2],
            remarks: row[3].toString()
          })
        );
      }
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
