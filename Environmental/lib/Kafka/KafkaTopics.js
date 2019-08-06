'use strict';

const client = require('./KafkaClient.js');

var topics = {
  ANTA_SOC_VISITORS_MONTHLY: {
    topic: 'anta_soc_visitors_monthly_draxis',
    partitions: 6,
    replicationFactor: 3
  },
  ANT_ENV_CITYOFANT_GWL: {
    topic: 'ant_env_cityofant_gwl_(draxis)',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_AIRQUALITY_ENVMIN_HOURLY: {
    topic: 'anta_env_airquality_envmin_hourly_draxis',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_WATERQUALITYFLOW_CITYOFANTALYA_MONTHLY: {
    topic: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_MET_W_DAILY: {
    topic: 'cork_env_met_w_daily',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_OPW_WL_15MIN: {
    topic: 'cork_env_opw_wl_15min_draxis',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_DAILY: {
    topic: 'cork_soc_visitors_daily_draxis',
    partitions: 6,
    replicationFactor: 3
  },
  CUTLER_THESS_SPEEDMEASUREMENTS: {
    topic: 'cutler_thess_speedmeasurements_1',
    partitions: 6,
    replicationFactor: 3
  },
  CUTLER_THESS_ENVPARAMETERS: {
    topic: 'cutler_thess_envparameters',
    partitions: 6,
    replicationFactor: 3
  },
  RAIN_1: {
    topic: 'rain_1',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_INTEGR_PARKING: {
    topic: 'cork_integr_parking',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_INTEGR_VISITORS: {
    topic: 'cork_integr_visitors',
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
