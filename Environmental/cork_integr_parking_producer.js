const XLSX = require('xlsx-extract').XLSX;

const kafka_producer = require('./lib/Kafka/KafkaProducer.js');
const kafka_topics = require('./lib/Kafka/KafkaTopics.js');

const topic = kafka_topics.topics.CORK_INTEGR_PARKING.topic;
var messages = [];

const createIndex = async () => {
  await client.indices.create({
    index: 'cork_integr_parking',
    body: {
      settings: {
        number_of_shards: 1
      }
    }
  });
};

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

// createIndex();

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/cork dash parking data.xlsx', {
      sheet_nr: 1,
      ignore_header: 1
    })
    .on('row', async row => {
      var returnVal = {
        'Parking Option': row[0],
        Spaces: row[1],
        Area: row[2],
        'Construction Cost': row[3],
        'Construction Cost per space': row[4],
        'Max visitors per day': row[5],
        'Revenues per space': row[6],
        'Revenues per day': row[7],
        'Revenues - Construction cost': row[8]
      };
      if (returnVal) {
        messages.push(JSON.stringify(returnVal));
      }
    })
    .on('end', function(err) {
      if (elBody.length) saveToElastic(elBody);
      console.log('Data succesfully indexed');
    });
})();
