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

*/

const { Client } = require('@elastic/elasticsearch');
const fs = require('fs');
const env = require('../config')

// Check is Elasticsearch is configured with SSL
// and make the appropriate ES client object (due to difference in http/https and certs)
// We make the assumption that if ES hasn't certifications, it also doesn't have username/password
if (env.ES_CA_CERTS == undefined) {
  var elasticClient = {
    node: `http://${env.ES_HOST}:${env.ES_PORT}`
  };
} else {
  var elasticClient = {
    node: `https://${env.ES_HOST}:${env.ES_PORT}`,
    auth: {
      username: env.ES_USER,
      password: env.ES_PASSWORD
    },
    ssl: {
      ca: fs.readFileSync(env.ES_CA_CERTS),
      rejectUnauthorized: true
    }
  }
}

// Init Elasticsearch client
elasticSearchclient = new Client(elasticClient);


const checkIfIndexExist = async index => {
  return new Promise(async resolve => {
    console.log(`Indexing ${index.index}`);
    elasticSearchclient.indices
      .create({
        index: index.index,
        body: {
          mappings: {
            // _doc: {
              properties: index.mapping
            // }
          }
        }
      })
      .then(res => {
        console.log(`Succesfully Created: ${index.index}`);
      })
      .catch(err => {
        console.log(err.body.error);
      });
  });
};

const initIndexes = (async (indexes) => {
  indexes.map(async index => {
    return await checkIfIndexExist(index);
  })
});

module.exports = initIndexes;