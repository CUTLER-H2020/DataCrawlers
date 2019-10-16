const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elIndex = {
  index: {
    _index: 'cork_integr_parking',
    _type: '_doc'
  }
};

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elBody = [];

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
  // return await client.bulk(
  //   {
  //     requestTimeout: 600000,
  //     body: elBody
  //   },
  //   function(err, resp) {
  //     if (err) console.log(err.response);
  //     else console.log('Data succesfully indexed!');
  //   }
  // );
  KafkaProducer(elBody, 'CORK_ENV_PARKING_PILOTINTEGR_ONCE');
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
        // elBody.push(elIndex);
        elBody.push(returnVal);
      }
    })
    .on('end', function(err) {
      if (elBody.length) saveToElastic(elBody);
      console.log('Data succesfully indexed');
    });
})();
