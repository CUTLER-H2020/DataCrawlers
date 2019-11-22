##This code is open-sourced software licensed under the MIT license
##Copyright 2019 Karypidis Paris - Alexandros, Democritus University of Thrace (DUTH)
##Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
##The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##
##DISCLAIMER
##This code is used to crawl/parse data from Eurostat databases. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.

"""
CUTLER H2020 Project
Python 3.5

The file contains a python dictionary with cities that script scrapes data
To fill a new city, use the same format as already exists
E.g. Key: "City name - Country", Value: "link taken from maps.me"
"""

cities = {
     "Thessaloniki - Greece": "country-ellada/city-thessaloniki-57554537",
     "Cork - Ireland": "country-ireland/city-cork-1422314245",
     "Antalya - Turkey": "country-turkiye/city-antalya-428039517/",
     "Antwerp - Belgium": "country-belgie---belgique---belgien/city-antwerpen-1765433658/"
}
