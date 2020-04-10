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

This code is used to crawl/parse data from file from Cork Municipality (cork_max_visitors_revenues_yearly).
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

*/

const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
const data = require('./files/cork_max_visitors_revenues_yearly');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elBody = [];

const saveToElastic = async elBody => {
  KafkaProducer(elBody, 'CORK_SOC_VISITORS_PILOTINTEGR_DAILY');
  return;
};

const extractValues = (async () => {
  data.map((d, i) => {
    if (i % 2 !== 0) {
      var returnVal = {
        date: moment(d['Date']).format('YYYY/MM/DD'),
        'No of Visitors': d['No of Visitors'],
        Revenues: d['Revenues']
      };
      if (returnVal) {
        // elBody.push(elIndex);
        elBody.push(returnVal);
      }
    }
  });

  if (elBody.length) saveToElastic(elBody);
})();
