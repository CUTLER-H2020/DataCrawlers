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

This code is used to crawl/parse data from several files from Thessaloniki Municipality (under folder /files/thess_speedmeasurements_files/).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx');
var greekUtils = require('greek-utils');
const moment = require('moment');
var fs = require('fs');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

fs.readdir(__dirname + '/files/thess_speedmeasurements_files', function(
  err,
  files
) {
  if (err) {
    console.error('Could not list the directory.', err);
    process.exit(1);
  }

  var elBody = [];
  files.map(file => {
    console.log('Opening file: ' + file);

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
        elBody.push({
          date: moment(row.Timestamp)
            .add(1, 'minute')
            .format('YYYY/MM/DD HH:mm:ss'),
          day: moment(row.Timestamp)
            .add(1, 'minute')
            .format('DD'),
          month: moment(row.Timestamp)
            .add(1, 'minute')
            .format('MM'),
          year: moment(row.Timestamp)
            .add(1, 'minute')
            .format('YYYY'),
          time: moment(row.Timestamp)
            .add(1, 'minute')
            .format('HH:mm'),
          id: row.PathID,
          name: row.Name ? greekUtils.toGreeklish(row.Name.split('. ')[1]) : '',
          speed: row.Value,
          samples: row.Samples,
          unit: 'u (km/h)',
          // mileage: row[2] * 5,
          mileage_unit: 'vkm (km*cars)'
        });
      });
    });
  });
  KafkaProducer(elBody, 'THESS_ENV_SPEEDMEASUREMENTS_15MIN');
});
