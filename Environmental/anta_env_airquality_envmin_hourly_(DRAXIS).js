const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
var breakpoints = require('../files/helpers/aqi_breakpoints');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'anta_env_airquality_envmin_hourly_draxis',
    _type: '_doc'
  }
};

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
    .extract(__dirname + '/anta_air_quality_2018-2019.xlsx', {
      sheet_nr: 0,
      ignore_header: 3
    })
    .on('row', function(row) {
      currentArray.push(row);
      dailyPM += row[2];
      if (
        parseInt(
          moment(row[1])
            .add(-1, 'hours')
            .format('HH')
        ) == 23
      ) {
        dailyPM = dailyPM / 24;
        let selectedBp = breakpoints.filter(bp => {
          return dailyPM <= bp['PM10'].high && dailyPM >= bp['PM10'].low;
        })[0];
        let pm10AQI = '';
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
              elBody.push(elIndex);
              elBody.push({
                station_name: 'Antalya Air Quality Station',
                station_location: {
                  lat: 36.8875,
                  lon: 30.726667
                },
                date: moment(row[0]).format('YYYY/MM/DD'),
                month: moment(row[0]).format('MM'),
                year: moment(row[0]).format('YYYY'),
                day: moment(row[0]).format('DD'),
                time: moment(row[1])
                  .add(-1, 'hours')
                  .format('HH:mm'),
                parameter_name: units[i - 2].pollutant,
                parameter_fullname: `${units[i - 2].pollutant} ${
                  units[i - 2].unit
                }`,
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
      client.indices.create(
        {
          index: 'anta_env_airquality_envmin_hourly_draxis',
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
        },
        (err, resp) => {
          if (err) console.log(err);
          client.bulk(
            {
              requestTimeout: 600000,
              body: elBody
            },
            function(err, resp) {
              if (err) console.log(err.response);
              else console.log('All files succesfully indexed!');
            }
          );
        }
      );
    });
})();
