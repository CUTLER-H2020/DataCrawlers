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

This code is used to crawl/parse data from file from Antalya Municipality (Visitor numbers.xlsx).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const moment = require('moment');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elBody = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/Visitor numbers.xlsx', {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      // elBody.push(elIndex);
      elBody.push({
        date: moment(row[0]).format('YYYY/MM/DD'),
        month: moment(row[0]).format('MM'),
        year: moment(row[0]).format('YYYY'),
        visitors: row[1] ? row[1] : null
      });
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'ANTA_SOC_VISITORS_MONTHLY');
    });
})();
