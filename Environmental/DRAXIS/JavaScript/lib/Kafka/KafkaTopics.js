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

var topics = {
  ANTA_SOC_VISITORS_MONTHLY: {
    topic: 'ANTA_SOC_VISITORS_MONTHLY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'ANTA_SOC_VISITORS_FINISH_MONTHLY',
    index: 'anta_soc_visitors_monthly_draxis',
    file: 'anta_soc_visitors_monthly.js'
  },
  ANTA_SOC_VISITORS_FINISH_MONTHLY: {
    topic: 'ANTA_SOC_VISITORS_FINISH_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_GWL_2MONTHS: {
    topic: 'ANTW_ENV_GWL_2MONTHS',
    partitions: 6,
    replicationFactor: 3,
    finish: 'ANTW_ENV_GWL_FINISH_2MONTHS',
    index: 'ant_env_cityofant_gwl_(draxis)',
    file: 'ant_env_cityofant_gwl_(draxis).js'
  },
  ANTW_ENV_GWL_FINISH_2MONTHS: {
    topic: 'ANTW_ENV_GWL_FINISH_2MONTHS',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_AIRQUALITY_HOURLY: {
    topic: 'ANTA_ENV_AIRQUALITY_HOURLY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'ANTA_ENV_AIRQUALITY_FINISH_HOURLY',
    index: 'anta_env_airquality_envmin_hourly_draxis',
    file: 'anta_env_airquality_envmin_hourly_(DRAXIS).js'
  },
  ANTA_ENV_AIRQUALITY_FINISH_HOURLY: {
    topic: 'ANTA_ENV_AIRQUALITY_FINISH_HOURLY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTA_ENV_WATERQUALITYFLOW_MONTHLY: {
    topic: 'ANTA_ENV_WATERQUALITYFLOW_MONTHLY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'ANTA_ENV_WATERQUALITYFLOW_FINISH_MONTHLY',
    index: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis',
    file: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis.js'
  },
  ANTA_ENV_WATERQUALITYFLOW_FINISH_MONTHLY: {
    topic: 'ANTA_ENV_WATERQUALITYFLOW_FINISH_MONTHLY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_MET_W_DAILY: {
    topic: 'CORK_ENV_MET_W_DAILY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'CORK_ENV_MET_W_FINISH_DAILY',
    index: 'cork_env_met_w_daily',
    file: 'cork_env_met_w_daily_draxis.js'
  },
  CORK_ENV_MET_W_FINISH_DAILY: {
    topic: 'CORK_ENV_MET_W_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_OPW_WL_15MIN: {
    topic: 'CORK_ENV_OPW_WL_15MIN',
    partitions: 6,
    replicationFactor: 3,
    finish: 'CORK_ENV_OPW_WL_FINISH_15MIN',
    index: 'cork_env_opw_wl_15min_draxis',
    file: 'CORK_ENV_OPW_WL_15min.js'
  },
  CORK_ENV_OPW_WL_FINISH_15MIN: {
    topic: 'CORK_ENV_OPW_WL_FINISH_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_DAILY: {
    topic: 'CORK_SOC_VISITORS_DAILY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'CORK_SOC_VISITORS_FINISH_DAILY',
    index: 'cork_soc_visitors_daily_draxis',
    file: 'cork_soc_visitors_daily_draxis.js'
  },
  CORK_SOC_VISITORS_FINISH_DAILY: {
    topic: 'CORK_SOC_VISITORS_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_SPEEDMEASUREMENTS_15MIN: {
    topic: 'THESS_ENV_SPEEDMEASUREMENTS_15MIN',
    partitions: 6,
    replicationFactor: 3,
    finish: 'THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN',
    index: 'cutler_thess_speedmeasurements_1',
    file: 'cutler_thess_speedmeasurements_draxis_1.js'
  },
  THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN: {
    topic: 'THESS_ENV_SPEEDMEASUREMENTS_FINISH_15MIN',
    partitions: 6,
    replicationFactor: 3
  },
  THESS_ENV_ENVPARAMETERS_DAILY_YEARLY: {
    topic: 'THESS_ENV_ENVPARAMETERS_DAILY_YEARLY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'THESS_ENV_ENVPARAMETERS_DAILY_FINISH_YEARLY',
    index: 'cutler_thess_envparameters',
    file: 'cutler_thess_envparameters.js'
  },
  THESS_ENV_ENVPARAMETERS_DAILY_FINISH_YEARLY: {
    topic: 'THESS_ENV_ENVPARAMETERS_DAILY_FINISH_YEARLY',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_ENV_PARKING_PILOTINTEGR_ONCE: {
    topic: 'CORK_ENV_PARKING_PILOTINTEGR_ONCE',
    partitions: 6,
    replicationFactor: 3,
    finish: 'CORK_ENV_PARKING_PILOTINTEGR_FINISH_ONCE',
    index: 'cork_integr_parking',
    file: 'cork_integr_parking.js'
  },
  CORK_ENV_PARKING_PILOTINTEGR_FINISH_ONCE: {
    topic: 'CORK_ENV_PARKING_PILOTINTEGR_FINISH_ONCE',
    partitions: 6,
    replicationFactor: 3
  },
  CORK_SOC_VISITORS_PILOTINTEGR_DAILY: {
    topic: 'CORK_SOC_VISITORS_PILOTINTEGR_DAILY',
    partitions: 6,
    replicationFactor: 3,
    finish: 'CORK_SOC_VISITORS_PILOTINTEGR_FINISH_DAILY',
    index: 'cork_integr_visitors',
    file: 'cork_integr_visitors.js'
  },
  CORK_SOC_VISITORS_PILOTINTEGR_FINISH_DAILY: {
    topic: 'CORK_SOC_VISITORS_PILOTINTEGR_FINISH_DAILY',
    partitions: 6,
    replicationFactor: 3
  },
  ANTW_ENV_HISTPREC_10MIN: {
    topic: 'ANTW_ENV_HISTPREC_10MIN',
    partitions: 6,
    replicationFactor: 3,
    finish: 'ANTW_ENV_HISTPREC_FINISH_10MIN',
    index: 'rain_1',
    file: 'rain_1.js'
  },
  ANTW_ENV_HISTPREC_FINISH_10MIN: {
    topic: 'ANTW_ENV_HISTPREC_FINISH_10MIN',
    partitions: 6,
    replicationFactor: 3
  }
};

var KafkaTopics = {
  topics: topics
};

module.exports = KafkaTopics;
