const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'ant_env_cityofant_gwl_(draxis)',
    _type: '_doc'
  }
};

var elBody = [];
var stations = [];

const saveToElastic = elBody => {
  client.bulk(
    {
      body: elBody
    },
    function(err, resp) {
      if (err) console.log(err);
      console.log('All files succesfully indexed!');
    }
  );
};

const extractStations = () => {
  let data = [];
  return new Promise((resolve, reject) => {
    new XLSX()
      .extract(__dirname + '/files/Export_CUTLER_v40.xlsx', {
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
        // elBody.push(elIndex);
        elBody.push({
          station_id: selectedStation[0].toString(),
          station_name: selectedStation[9].toString(),
          station_location: {
            lat: selectedStation[11],
            lon: selectedStation[10]
          },
          date: row[1],
          peil_cor: row[2],
          remarks: row[3].toString()
        });
      }
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'ANTW_ENV_GWL_2MONTHS');
      // client.indices.create(
      //   {
      //     index: 'ant_env_cityofant_gwl_(draxis)',
      //     body: {
      //       settings: {
      //         number_of_shards: 1
      //       },
      //       mappings: {
      //         _doc: {
      //           properties: {
      //             station_location: {
      //               type: 'geo_point'
      //             }
      //           }
      //         }
      //       }
      //     }
      //   },
      //   (err, resp) => {
      //     if (err) console.log(err);
      //     client.bulk(
      //       {
      //         requestTimeout: 600000,
      //         body: elBody
      //       },
      //       function(err, resp) {
      //         if (err) console.log(err.response);
      //         else console.log('All files succesfully indexed!');
      //       }
      //     );
      //   }
      // );
    });
})();
