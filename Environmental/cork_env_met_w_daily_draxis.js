const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

const client = new elasticsearch.Client({
  host: '10.10.2.51:9092'
});

var elIndex = {
  index: {
    _index: 'cork_env_met_w_daily',
    _type: '_doc'
  }
};

var elBody = [];
const metrics = [
  { code: 'date', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'maxtp', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'mintp', description: '', unit: '' },
  { code: 'igmin', description: '', unit: '' },
  { code: 'gmin', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  { code: 'rain', description: 'Precipitation', unit: 'mm' },
  { code: 'cbl', description: '', unit: '' },
  { code: 'wdsp', description: 'Mean Wind Speed', unit: 'kt' },
  { code: 'ind', description: '', unit: '' },
  { code: 'hm', description: '', unit: '' },
  { code: 'ind', description: '', unit: '' },
  {
    code: 'ddhm',
    description: 'Wind Direction at max 10 min mean',
    unit: 'deg'
  },
  { code: 'ind', description: '', unit: '' },
  { code: 'hg', description: '', unit: '' },
  { code: 'soil', description: 'Temperature', unit: 'C' },
  { code: 'pe', description: '', unit: '' },
  { code: 'evap', description: '', unit: '' },
  { code: 'smd_wd', description: '', unit: '' },
  { code: 'smd_md', description: '', unit: '' },
  { code: 'smd_pd', description: '', unit: '' },
  { code: 'glorad', description: '', unit: '' }
];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/CORK_ENV_MET_W_DAILY.xlsx', {
      sheet_nr: 0,
      ignore_header: 22
    })
    .on('row', function(row) {
      row.map((r, i) => {
        if (i == 8 || i == 17 || i == 10 || i == 14) {
          // console.log(r);
          // console.log(row[0]);
          // console.log(metrics[i]);
          // elBody.push(elIndex);
          elBody.push({
            station_name: 'ROCHES POINT',
            station_location: {
              lat: 51.789,
              lon: -8.24
            },
            date: moment(row[0]).format('YYYY/MM/DD'),
            month: moment(row[0]).format('MM'),
            year: moment(row[0]).format('YYYY'),
            parameter: metrics[i].code,
            parameter_description: metrics[i].description,
            parameter_unit: metrics[i].unit,
            parameter_full_name: `${metrics[i].description} (${metrics[i].unit})`,
            value: parseFloat(r)
          });
        }
      });
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'CORK_ENV_MET_W_DAILY');
      // client.indices.create(
      //   {
      //     index: 'cork_env_met_w_daily',
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
