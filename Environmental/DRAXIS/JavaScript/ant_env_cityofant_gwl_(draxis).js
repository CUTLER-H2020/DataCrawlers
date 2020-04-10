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

This code is used to crawl/parse data from file from Antwerp Municipality (Export_CUTLER_v40.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;

const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

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
  
  var elBody = [];

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
        
        let lat = selectedStation[11];
        let lon = selectedStation[10];
        
        // Some stations in excel don't have coordinates in WGS84 column
        if (lat == undefined || lon == undefined){
          stationLocation = null;
        } else {
          stationLocation = {
            lat: lat,
            lon: lon
          }
        }
        
        let data = {
          station_id: selectedStation[0].toString(),
          station_name: selectedStation[9].toString(),
          station_location: stationLocation,
          date: row[1],
          peil_cor: row[2],
          remarks: row[3].toString()
        };
        
        console.log(data);
        elBody.push(data);
      }
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'ANTW_ENV_GWL_2MONTHS');
    });
})();
