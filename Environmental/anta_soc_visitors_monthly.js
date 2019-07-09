const XLSX = require('xlsx-extract').XLSX;
const elasticsearch = require('elasticsearch');
const moment = require('moment');

const client = new elasticsearch.Client({
  host: 'localhost:9200'
});

var elIndex = {
  index: {
    _index: 'anta_soc_visitors_monthly_draxis',
    _type: '_doc'
  }
};

var elBody = [];

const extractValues = (async () => {
  console.log('Opening file');
  new XLSX()
    .extract(__dirname + '/files/Visitor numbers.xlsx', {
      sheet_nr: 0,
      ignore_header: 1
    })
    .on('row', function(row) {
      elBody.push(elIndex);
      elBody.push({
        date: moment(row[0]).format('YYYY/MM/DD'),
        month: moment(row[0]).format('MM'),
        year: moment(row[0]).format('YYYY'),
        visitors: row[1] ? row[1] : '-'
      });
    })
    .on('end', function(err) {
      console.log('Saving to elastic');
      client.indices.create(
        {
          index: 'anta_soc_visitors_monthly_draxis',
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
          if (err) console.log(err);
          client.bulk(
            {
              requestTimeout: 600000,
              body: elBody
            },
            function(err, resp) {
              if (err) console.log(err.response);
              else console.log('All files succesfully indexed!');
            }
          );
        }
      );
    });
})();
