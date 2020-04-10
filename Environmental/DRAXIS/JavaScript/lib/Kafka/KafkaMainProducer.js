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

const { Kafka } = require('kafkajs');
const fs = require('fs');
const env = require('../config')

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

// Init Kafka client
const kafka = new Kafka({
  clientId: 'cutler',
  brokers: [`${env.KAFKA_HOST}:${env.KAFKA_PORT}`],
  ssl: kafkaSSLConfig
});


const producer = kafka.producer();

const _ = require('lodash');

const KafkaTopics = require('./KafkaTopics');

const chunkNumber = 1000;
var count = 0;
var sendCount = 0;
module.exports = (msg, topicName) => {
  const broadcastMessageToKafka = (message, i) => {
    producer
      .send({
        topic: topicName,
        messages: message.map(mes => {
          return { value: JSON.stringify(mes) };
        })
      })
      .then(res => {
        sendCount += message.length;
        console.log(
          `Broadcasted ${message.length} in count ${sendCount} of ${count} messages`
        );
      })
      .catch(err => console.log(err));

    count += message.length;
  };

  console.log('Sending... Before');

  producer
    .connect()
    .then(res => {
      console.log('Producer Connected');
      Promise.all(
        _.chunk(msg, chunkNumber).map(async (m, i) => {
          return await broadcastMessageToKafka(m, i);
        })
      );
    })
    .catch(err => console.log(err));
  console.log('Succesfully Broadcast All messages!');
  console.log('Broadcasting to finish!');
  console.log(`Broadcasted ${count} messages`);

  producer.send({
    topic: KafkaTopics.topics[topicName].finish,
    messages: [
      {value: 'FINISHED!'}
    ]
  })
  .then(res => console.log(res))
  .catch(err => console.log(err))
};
