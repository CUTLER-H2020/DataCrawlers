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

const initIndices = require('./CreateAllIndexes');

const indexes = [
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
    index: 'cork_integr_visitors',
    mapping: {
      date: {
        type: 'date',
        format: 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis'
      }
    }
  },
  {
    index: 'cork_integr_parking',
    mapping: {}
  },
]

Promise.resolve(initIndices(indexes));