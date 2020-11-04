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
      aa: {
        type: "long"
      },
      daily_aqi: {
        type: "long"
      },
      date: {
        type: "date",
        format: "yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis"
      },
      loc: {
        type: "geo_point"
      },
      month_: {
        type: "long"
      },
      parameter_fullname: {
        type: "text",
        fields: {
          keyword: {
            type: "keyword",
            ignore_above: 256
          }
        }
      },
      parameter_name: {
        type: "text",
        fields: {
          keyword: {
            type: "keyword",
            ignore_above: 256
          }
        }
      },
      station_name: {
        type: "text",
        fields: {
          keyword: {
            type: "keyword",
            ignore_above: 256
          }
        }
      },
      units: {
        type: "text",
        fields: {
          keyword: {
            type: "keyword",
            ignore_above: 256
          }
        }
      },
      value: {
        type: "long"
      },
      year_: {
        type: "long"
      }
    }
  }
]

Promise.resolve(initIndices(indexes));