'use strict';

const indexes = [
  {
    index: 'anta_soc_visitors_monthly_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      month: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      station_location: {
        type: 'geo_point'
      },
      visitors: {
        type: 'long'
      },
      year: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'ant_env_cityofant_gwl_(draxis)',
    mapping: {
      date: {
        type: 'date'
      },
      station_location: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'anta_env_airquality_envmin_hourly_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      station_location: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'anta_env_waterqualityflow_cityofantalya_monthly_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      station_location: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'cork_env_met_w_daily',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      month: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parameter: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parameter_description: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parameter_full_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parameter_unit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      station_location: {
        type: 'geo_point'
      },
      station_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      value: {
        type: 'float'
      },
      year: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cork_env_opw_wl_15min_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm||yyyy/MM/dd||epoch_millis'
      },
      date_hour: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      hour: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      month: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      station_location: {
        type: 'geo_point'
      },
      station_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      unit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      water_level: {
        type: 'float'
      },
      year: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cork_soc_visitors_daily_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      incomes: {
        type: 'long'
      },
      month: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      pay_visitors: {
        type: 'long'
      },
      station_location: {
        type: 'geo_point'
      },
      ticker_unit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      ticket_price: {
        type: 'long'
      },
      visitors: {
        type: 'long'
      },
      year: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'anta_soc_visitors_monthly_draxis',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      station_location: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'cutler_thess_speedmeasurements_1',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      id: {
        type: 'long'
      },
      mileage: {
        type: 'float'
      },
      mileage_unit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      samples: {
        type: 'long'
      },
      speed: {
        type: 'long'
      },
      unit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cutler_thess_envparameters',
    mapping: {
      aa: {
        type: 'long'
      },
      daily_aqi: {
        type: 'long'
      },
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      loc: {
        type: 'geo_point'
      },
      month_: {
        type: 'long'
      },
      parameter_fullname: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parameter_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      station_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      units: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      value: {
        type: 'long'
      },
      year_: {
        type: 'long'
      }
    }
  },
  {
    index: 'rain_1',
    mapping: {
      code: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      measurement: {
        type: 'long'
      },
      station_location: {
        type: 'geo_point'
      },
      station_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cork_integr_visitors',
    mapping: {
      'No of Visitors': {
        type: 'long'
      },
      Revenues: {
        type: 'long'
      },
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      }
    }
  },
  {
    index: 'cork_integr_svr',
    mapping: {
      Revenue: {
        type: 'long'
      },
      Visitors: {
        type: 'long'
      },
      'Working Period of the Fort': {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cork_integr_parking',
    mapping: {
      Area: {
        type: 'long'
      },
      'Construction Cost': {
        type: 'long'
      },
      'Construction Cost per space': {
        type: 'long'
      },
      'Max visitors per day': {
        type: 'long'
      },
      'Parking Option': {
        type: 'long'
      },
      'Revenues - Construction cost': {
        type: 'long'
      },
      'Revenues per day': {
        type: 'long'
      },
      'Revenues per space': {
        type: 'long'
      },
      Spaces: {
        type: 'long'
      }
    }
  },
  {
    index: 'cork_integr_social',
    mapping: {
      city: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      full_text: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      hashtags: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      location: {
        type: 'geo_point'
      },
      retweet_count: {
        type: 'long'
      },
      sentiment: {
        type: 'float'
      },
      user: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  },
  {
    index: 'cork_integr_survey',
    mapping: {
      access: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      accessissues: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      accessissuesyn: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      accessthoughout: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      add_entrance_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      aspects_changed: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      aspects_improved: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      bath_facilities: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      cafe: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      cityguidedtours_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_access: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_cafe: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_parking: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_siteattractions: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_ticket: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_toilet: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      comment_tourguide: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      count: {
        type: 'long'
      },
      created_date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm||yyyy/MM/dd||epoch_millis'
      },
      jointtour_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      location: {
        type: 'geo_point'
      },
      offsite_parking_exp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      offsite_parking_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      onsite_parking_exp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      onsite_parking_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      origin: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parkandridecline_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parking_exp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parkingelaborate: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      parkingonly: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      process_name: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      reasonvisit: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      reference: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      sea_access_imp: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      sentiment_parking: {
        type: 'float'
      },
      site_attractions: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      standout_attraction: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      ticket_office: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      toilet_facilities: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      tour_guides: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      visitingparty: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      },
      visitwhen: {
        type: 'text',
        fields: {
          keyword: {
            type: 'keyword',
            ignore_above: 256
          }
        }
      }
    }
  }
];

const ElasticsearchIndexes = {
  indexes
};

module.exports = ElasticsearchIndexes;
