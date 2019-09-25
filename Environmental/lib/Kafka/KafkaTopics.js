'use strict';

const client = require('./KafkaClient.js');

var topics = {
  ANTA_SOC_VISITORS_MONTHLY: {
    topic: 'ANTA_SOC_VISITORS_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_SOC_VISITORS_FINISH_MONTHLY: {
    topic: 'ANTA_SOC_VISITORS_FINISH_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_GWL_2MONTHS: {
    topic: 'ANTW_ENV_GWL_2MONTHS',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_GWL_FINISH_2MONTHS: {
    topic: 'ANTW_ENV_GWL_FINISH_2MONTHS',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_AIRQUALITY_HOURLY: {
    topic: 'ANTA_ENV_AIRQUALITY_HOURLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_AIRQUALITY_FINISH_HOURLY: {
    topic: 'ANTA_ENV_AIRQUALITY_FINISH_HOURLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_WATERQUALITYFLOW_MONTHLY: {
    topic: 'ANTA_ENV_WATERQUALITYFLOW_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_WATERQUALITYFLOW_FINISH_MONTHLY: {
    topic: 'ANTA_ENV_WATERQUALITYFLOW_FINISH_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_MET_W_DAILY: {
    topic: 'CORK_ENV_MET_W_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_MET_W_FINISH_DAILY: {
    topic: 'CORK_ENV_MET_W_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_OPW_WL_15MIN: {
    topic: 'CORK_ENV_OPW_WL_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_OPW_WL_FINISH_15MIN: {
    topic: 'CORK_ENV_OPW_WL_FINISH_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_DAILY: {
    topic: 'CORK_SOC_VISITORS_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_FINISH_DAILY: {
    topic: 'CORK_SOC_VISITORS_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_SPEEDMEASUREMENTS_15MIN: {
    topic: 'THESS_ENV_SPEEDMEASUREMENTS_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN: {
    topic: 'THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_ENVPARAMETERS_DAILY_YEARLY: {
    topic: 'THESS_ENV_ENVPARAMETERS_DAILY_YEARLY',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_ENVPARAMETERS_DAILY_FINISH_YEARLY: {
    topic: 'THESS_ENV_ENVPARAMETERS_DAILY_FINISH_YEARLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_HISTPREC_10MIN: {
    topic: 'ANTW_ENV_HISTPREC_10MIN',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_HISTPREC_FINISH_10MIN: {
    topic: 'ANTW_ENV_HISTPREC_FINISH_10MIN',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_PARKING_PILOTINTEGR_ONCE: {
    topic: 'CORK_ENV_PARKING_PILOTINTEGR_ONCE',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_PARKING_PILOTINTEGR_FINISH_ONCE: {
    topic: 'CORK_ENV_PARKING_PILOTINTEGR_FINISH_ONCE',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_PILOTINTEGR_DAILY: {
    topic: 'CORK_SOC_VISITORS_PILOTINTEGR_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_PILOTINTEGR_FINISH_DAILY: {
    topic: 'CORK_SOC_VISITORS_PILOTINTEGR_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  }
};

var KafkaTopics = {
  client: client,
  topics: topics,
  createAll: (callback = () => {}) => {
    console.info('Creating all topics in Kafka');

    var topicsToCreate = Object.values(topics);

    topicsToCreate.forEach(topic => {
      console.info(
        'Creating ' +
          topic.topic +
          ' (partitions: ' +
          topic.partitions +
          ', replicationFactor:' +
          topic.replicationFactor +
          ')'
      );
    });

    client.createTopics(topicsToCreate, callback);
  }
};

module.exports = KafkaTopics;
