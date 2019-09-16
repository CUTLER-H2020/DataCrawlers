'use strict';

require('dotenv').config();

const elasticsearch = require('elasticsearch');

// create new client
const ElasticSearchClient = new elasticsearch.Client({
    host: process.env.ELASTICSEARCH_HOST,
    log: 'error'
});

module.exports = ElasticSearchClient;
