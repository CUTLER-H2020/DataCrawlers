// const XLSX = require('xlsx-extract').XLSX;
const XLSX = require('xlsx');

const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'cutler_thess_speedmeasurements_1',
    _type: '_doc'
  }
};

client.indices.create(
  {
    index: 'cork_soc_visitors_daily_draxis',
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
    // if (err) console.log(err);
    console.log('Index Created Succesfully');
  }
);

fs.readdir(__dirname + '/files', function(err, files) {
  if (err) {
    console.error('Could not list the directory.', err);
    process.exit(1);
  }

  files.map(file => {
    console.log('Opening file: ' + file);
    var elBody = [];

    var workbook = XLSX.readFile(
      __dirname + '/files/thess_speedmeasurements_files/' + file,
      {
        type: 'binary',
        cellDates: true,
        cellStyles: true
      }
    );

    workbook.SheetNames.map(sheet => {
      // console.log(workbook.Sheets[sheet]);
      var xlData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet]);

      xlData.map(row => {
        // console.log(row);
        // console.log(row.Timestamp);
        // console.log(
        //   moment(row.Timestamp)
        //     .add(1, 'minute')
        //     .format('YYYY/MM/DD HH:mm')
        // );
        // console.log(
        //   moment(row.Timestamp)
        //     .add(1, 'minute')
        //     .add(-2, 'hours')
        //     .format('YYYY/MM/DD HH:mm')
        // );

        elBody.push(elIndex);
        elBody.push({
          date: moment(row.Timestamp).format('YYYY/MM/DD HH:mm'),
          day: moment(row.Timestamp).format('DD'),
          month: moment(row.Timestamp).format('MM'),
          year: moment(row.Timestamp).format('YYYY'),
          time: moment(row.Timestamp).format('HH:mm'),
          id: row.PathID,
          name: row.Name ? row.Name.split('. ')[1] : '',
          speed: row.Value,
          samples: row.Samples,
          unit: 'u (km/h)',
          // mileage: row[2] * 5,
          mileage_unit: 'vkm (km*cars)'
        });
      });
    });

    client.bulk(
      {
        requestTimeout: 600000,
        body: elBody
      },
      function(err, resp) {
        if (err) console.log(err.response);
        else console.log('All files for ' + file + ' succesfully indexed!');
      }
    );
  });
});
