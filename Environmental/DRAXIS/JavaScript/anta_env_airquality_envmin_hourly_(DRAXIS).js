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

This code is used to crawl/parse data from file from Antalya Municipality (anta_air_quality_2018-2019.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');
var breakpoints = require('./files/helpers/aqi_breakpoints');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');


const units = [
  { pollutant: 'PM10', unit: 'µg/m³' },
  { pollutant: 'SO2', unit: 'µg/m³' },
  { pollutant: 'Air Temperature', unit: '°C' },
  { pollutant: 'Wind Direction', unit: 'Derece' },
  { pollutant: 'Wind Speed', unit: 'm/s' },
  { pollutant: 'Relative Humidity', unit: '%' },
  { pollutant: 'Air Pressure', unit: 'mbar' }
];

var elBody = [];
var currentArray = [];
var dailyPM = 0;

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/anta_air_quality_2018-2019.xlsx', {
      sheet_nr: 0,
      ignore_header: 3,
      ignore_timezone: true
    })
    .on('row', function(row) {
      currentArray.push(row);
      dailyPM += row[2];
      if (parseInt(moment(row[1]).format('HH')) == 23) {
        dailyPM = dailyPM / 24;
        let selectedBp = breakpoints.filter(bp => {
          return dailyPM <= bp['PM10'].high && dailyPM >= bp['PM10'].low;
        })[0];
        // Make it null instead of empty string, when there's no selectedBp
        // in order Kibana's scripted field to work
        // let pm10AQI = '';
        let pm10AQI = null;
        if (selectedBp) {
          pm10AQI =
            ((selectedBp['AQI'].high - selectedBp['AQI'].low) /
              (selectedBp['PM10'].high - selectedBp['PM10'].low)) *
              (dailyPM - selectedBp['PM10'].low) +
            selectedBp['AQI'].low;
          pm10AQI = parseFloat(pm10AQI.toFixed(0));
        }

        currentArray.map((row, i) => {
          row.map((r, i) => {
            if (i > 1) {
              // elBody.push(elIndex);
              elBody.push({
                station_name: 'Antalya Air Quality Station',
                station_location: {
                  lat: 36.8875,
                  lon: 30.726667
                },
                // include 'time' in the 'date' field for Kibana's date range
                date: moment(row[0]).format('YYYY/MM/DD') + " " + moment(row[1]).format('HH:mm:ss'),
                month: moment(row[0]).format('MM'),
                year: moment(row[0]).format('YYYY'),
                day: moment(row[0]).format('DD'),
                time: moment(row[1]).format('HH:mm'),
                parameter_name: units[i - 2].pollutant,
                parameter_fullname: `${units[i - 2].pollutant} ${units[i - 2].unit}`,
                unit: units[i - 2].unit,
                value: r,
                daily_aqi: pm10AQI
              });
            }
          });
        });
        currentArray = [];
        dailyPM = 0;
      }
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'ANTA_ENV_AIRQUALITY_HOURLY');
    });
})();
