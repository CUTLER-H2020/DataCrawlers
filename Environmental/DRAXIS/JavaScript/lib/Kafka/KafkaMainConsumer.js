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

'use strict';

const { Client } = require('@elastic/elasticsearch');
const { Kafka } = require('kafkajs');
const fs = require('fs');
const env = require('../config')

// Check is Kafka is configured with SSL
// and make the appropriate configuration object
if (env.KAFKA_CERT_FILE == undefined){
  var kafkaSSLConfig = null;
} else {
  var kafkaSSLConfig = {
    rejectUnauthorized: true,
    ca: [fs.readFileSync(env.KAFKA_CA_FILE)],
    key: fs.readFileSync(env.KAFKA_KEY_FILE),
    cert: fs.readFileSync(env.KAFKA_CERT_FILE)
  };
}

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

// Init Kafka client
const kafka = new Kafka({
  clientId: 'cutler',
  brokers: [`${env.KAFKA_HOST}:${env.KAFKA_PORT}`],
  ssl: kafkaSSLConfig
});

// Init Elasticsearch client
const elasticSearchclient = new Client(elasticClient);

const topics = require('./KafkaTopics');
const consumer = kafka.consumer({ groupId: 'kaf-data' });

consumer.connect();

var consumerTopics = [];
Object.values(topics.topics).map(async ({ topic }, index) => {
  await consumer.subscribe({ topic: topic });
  consumerTopics.push({ topic: topic, partition: 0 });
});

var count = 1;

consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    if (topics.topics[topic].finish) {
      var item = JSON.parse(message.value.toString());
      
      await elasticSearchclient
        .index({
          index: topics.topics[topic].index,
          type: '_doc',
          body: item
        })
        .then(res => {
          console.log({
            count: count
          });
          count++;
        })
        .catch(err => {
          console.log(err.meta.body.error);
        });
    }
  }
});
