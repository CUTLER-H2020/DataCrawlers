const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
var breakpoints = require('./files/helpers/aqi_breakpoints');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis',
    _type: '_doc'
  }
};

const units = [
  { pollutant: 'BOD', unit: 'mg/L', DL: 5 },
  { pollutant: 'Dissolved Oxygen', unit: 'mg/L' },
  { pollutant: 'Fecal coliform', unit: 'CFU/100mL' },
  { pollutant: 'Fecal Streptococcus', unit: 'CFU/100mL' },
  { pollutant: 'COD', unit: 'mg/L', DL: 5 },
  { pollutant: 'pH' },
  { pollutant: 'Total Nitrogen', unit: 'mg/L', DL: 1.32 },
  { pollutant: 'Total Coliform', unit: 'CFU/100mL' },
  { pollutant: 'Total Phosphorus', unit: 'mg/L', DL: 0.025 },
  { pollutant: 'Depth', unit: 'm3/sec' },
  { pollutant: 'Flow', unit: 'm/sec' }
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

          // elBody.push(elIndex);
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
      // client.indices.create(
      //   {
      //     index: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis',
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
