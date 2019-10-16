const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
const stations = require('./files/stations');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elIndex = {
  index: {
    _index: 'rain_1',
    _type: '_doc'
  }
};

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elBody = [];

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
  KafkaProducer(elBody, 'ANTW_ENV_HISTPREC_10MIN');

  return;
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

// createIndex();

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
            // elBody.push(elIndex);
            elBody.push(returnVal);
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
      if (elBody.length) saveToElastic(index, elBody);
      console.log('Rain succesfully indexed');
    });
})();
