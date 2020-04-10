/**
This code is open-sourced software licensed under the MIT license. (http://opensource.org/licenses/MIT)

Copyright 2020 Stergios Bampakis, DRAXIS ENVIRONMENTAL S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

DISCLAIMER

This code is used to crawl/parse data from several files from Thessaloniki Municipality (stations_alladata_v21_deel1, stations_alladata_v20_deel2).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');
const stations = require('./files/stations_alladata_v21_deel1');
// const stations = require('./files/stations_alladata_v20_deel2');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

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
};

const extractValues = (async () => {
  let index = 0;
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/alladata_v21_deel1.xlsx', {
      // .extract(__dirname + '/files/alladata_v20_deel2.xlsx', {
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
