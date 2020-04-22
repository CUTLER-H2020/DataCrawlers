const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
var fs = require('fs');
var path = require('path');
var greekUtils = require('greek-utils');
const data = require('./files/cork_max_visitors_revenues_yearly');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

var elIndex = {
  index: {
    _index: 'cork_integr_visitors',
    _type: '_doc'
  }
};

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elBody = [];

const saveToElastic = async elBody => {

  KafkaProducer(elBody, 'CORK_SOC_VISITORS_PILOTINTEGR_DAILY');
  return;
  return await client.bulk(
    {
      requestTimeout: 600000,
      body: elBody
    },
    function(err, resp) {
      if (err) console.log(err.response);
      else console.log('Data succesfully indexed!');
    }
  );
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
