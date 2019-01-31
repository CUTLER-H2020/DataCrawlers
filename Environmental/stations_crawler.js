const XLSX = require('xlsx');
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

fs.readdir(__dirname + '/files', function(err, files) {
  if (err) {
    console.error('Could not list the directory.', err);
    process.exit(1);
  }

  var locations = {
    EGNATIAS: { lat: 40.623814599999996, lon: 22.953126999999995 },
    MARTIOY: { lat: 40.61637939999999, lon: 22.982339000000024 },
    LAGKADA: { lat: 40.64398020000002, lon: 22.958314700000074 },
    EPTAPYRGIOY: { lat: 40.65176230000001, lon: 22.93485439999995 },
    MALAKOPHS: { lat: 40.60102300000002, lon: 22.960178600000063 },
    DHMARXEIOY: { lat: 40.63753080000001, lon: 22.940941000000066 }
  };

  var elIndex = { index: { _index: 'cutlerdev', _type: '_doc' } };
  var elBody = [];

  files.forEach(function(file, index) {
    console.log('Indexing: ' + file);
    var workbook = XLSX.readFile(__dirname + '/files/' + file, {
      type: 'binary',
      cellDates: true,
      cellStyles: true
    });
    var sheet_name_list = workbook.SheetNames;

    sheet_name_list.map((val, index) => {
      if (val.split('Στ. ')[1]) {
        var xlData = XLSX.utils.sheet_to_json(
          workbook.Sheets[sheet_name_list[index]]
        );

        xlData.forEach(res => {
          var values = {};
          for (var key in res) {
            if (
              key.replace(' -', '').replace('\r\n', '') != 'A.A.' &&
              key.replace(' -', '').replace('\r\n', '') != 'Ημέρα' &&
              key
                .replace(' -', '')
                .replace('\r\n', '')
                .indexOf('Στ. ') < 0 &&
              key
                .replace(' -', '')
                .replace('\r\n', '')
                .indexOf('Σταθμός') < 0 &&
              key.replace(' -', '').replace('\r\n', '') != 'Ημερομηνία'
            ) {
              var splited = key.split('\r\n');
              var name;
              var coords = {
                lat: '',
                lon: ''
              };

              if (splited.length > 2) {
                name = splited[0] + ' ' + splited[1];
              } else {
                name = splited[0];
              }

              if (
                greekUtils.toGreeklish(val.split('Στ. ')[1]).split(' ').length >
                  1 &&
                locations[
                  greekUtils.toGreeklish(val.split('Στ. ')[1]).split(' ')[1]
                ]
              ) {
                coords =
                  locations[
                    greekUtils.toGreeklish(val.split('Στ. ')[1]).split(' ')[1]
                  ];
              } else if (
                locations[greekUtils.toGreeklish(val.split('Στ. ')[1])]
              ) {
                coords =
                  locations[greekUtils.toGreeklish(val.split('Στ. ')[1])];
              }

              var returnVal = {
                name: greekUtils.toGreeklish(val.split('Στ. ')[1]),
                loc: {
                  lat: coords.lat,
                  lon: coords.lon
                },
                date: moment(res['Ημερο -\r\nμηνία']).format('YYYY/MM/DD'),
                month_: parseInt(moment(res['Ημερο -\r\nμηνία']).format('MM')),
                year_: parseInt(moment(res['Ημερο -\r\nμηνία']).format('YYYY')),
                aa: res['A.A.'],
                measurment: name.replace(' - ', ''),
                value:
                  parseInt(res[key]) % 1 === 0 ? res[key] : parseInt(res[key]),
                unit: splited.length > 2 ? splited[2] : splited[1]
              };

              if (returnVal.value) {
                elBody.push(elIndex);
                elBody.push(returnVal);
              }
            }
          }
        });
      }
      //end assignment
      //end of promise
    });
  });

  client.bulk(
    {
      body: elBody
    },
    function(err, resp) {
      console.log('All files succesfully indexed!');
    }
  );
});
