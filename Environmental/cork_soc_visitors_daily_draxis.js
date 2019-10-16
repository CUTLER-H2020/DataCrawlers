const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');
const KafkaProducer = require('./lib/Kafka/KafkaMainProducer');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'cork_soc_visitors_daily_draxis',
    _type: '_doc'
  }
};

var elBody = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/visitor_numbers_cork.xlsx', {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      // elBody.push(elIndex);
      elBody.push({
        date: moment(row[0]).format('YYYY/MM/DD'),
        month: moment(row[0]).format('MM'),
        year: moment(row[0]).format('YYYY'),
        visitors: row[1],
        pay_visitors: row[2],
        ticket_price: 5,
        ticker_unit: 'euro',
        incomes: row[2] * 5
      });
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      KafkaProducer(elBody, 'CORK_SOC_VISITORS_DAILY');
      // client.indices.create(
      //   {
      //     index: 'cork_soc_visitors_daily_draxis',
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
