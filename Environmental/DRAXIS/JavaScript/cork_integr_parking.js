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

This code is used to crawl/parse data from file from Cork Municipality (cork dash parking data.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elBody = [];

const createIndex = async () => {
  await client.indices.create({
    index: 'cork_integr_parking',
    body: {
      settings: {
        number_of_shards: 1
      }
    }
  });
};

const saveToElastic = async elBody => {
  KafkaProducer(elBody, 'CORK_ENV_PARKING_PILOTINTEGR_ONCE');
};

// createIndex();

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/cork dash parking data.xlsx', {
      sheet_nr: 1,
      ignore_header: 1
    })
    .on('row', async row => {
      var returnVal = {
        'Parking Option': row[0],
        Spaces: row[1],
        Area: row[2],
        'Construction Cost': row[3],
        'Construction Cost per space': row[4],
        'Max visitors per day': row[5],
        'Revenues per space': row[6],
        'Revenues per day': row[7],
        'Revenues - Construction cost': row[8]
      };
      if (returnVal) {
        // elBody.push(elIndex);
        elBody.push(returnVal);
      }
    })
    .on('end', function(err) {
      if (elBody.length) saveToElastic(elBody);
      console.log('Data succesfully indexed');
    });
})();
