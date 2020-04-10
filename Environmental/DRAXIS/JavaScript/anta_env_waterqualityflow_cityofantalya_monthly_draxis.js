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

This code is used to crawl/parse data from file from Antalya Municipality (anta_water_quality_flow_2018_2019.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

const units = [
  { pollutant: 'BOD', unit: 'mg/L', DL: 5 },
  { pollutant: 'Dissolved Oxygen', unit: 'mg/L' },
  { pollutant: 'Fecal coliform', unit: 'CFU/100mL' },
  { pollutant: 'Fecal Streptococcus', unit: 'CFU/100mL' },
  { pollutant: 'COD', unit: 'mg/L', DL: 5 },
  { pollutant: 'pH', unit: '' },
  { pollutant: 'Total Nitrogen', unit: 'mg/L', DL: 1.32 },
  { pollutant: 'Total Coliform', unit: 'CFU/100mL' },
  { pollutant: 'Total Phosphorus', unit: 'mg/L', DL: 0.025 },
  { pollutant: 'Volumetric Flow', unit: 'm3/sec' },
  { pollutant: 'Water Velocity', unit: 'm/sec' }
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

          elBody.push({
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
            parameter_fullname: `${units[i - 4].pollutant} ${units[i - 4].unit}`,
            unit: units[i - 4].unit,
            value: r
          });
        }
      });
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'ANTA_ENV_WATERQUALITYFLOW_MONTHLY');
    });
})();
