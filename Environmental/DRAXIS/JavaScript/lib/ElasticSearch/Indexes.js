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
      station_location: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'cork_env_opw_wl_15min_draxis',
    mapping: {
      station_location: {
        type: 'geo_point'
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
      }
    }
  },
  {
    index: 'cutler_thess_envparameters',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      },
      loc: {
        type: 'geo_point'
      }
    }
  },
  {
    index: 'rain_1',
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
    index: 'cork_integr_visitors',
    mapping: {
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
    mapping: {}
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
