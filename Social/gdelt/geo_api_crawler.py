# -*- coding: utf-8 -*-
import requests

from cutler_cities import cities
from gdelt_es import *

class GeoApiCrawler:
    """
    A class for the retrieval of data from the GDELT Geo API.
    See https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ for a documentation of the Geo API
    """
    _base_url = "https://api.gdeltproject.org/api/v2/geo/geo"

    def __init__(self, es_host=None, es_port=None, es_hosts=None):
        """
        Initializes the GDELT Elasticsearch wrapper and the Elasticsearch relationship.
        If no keywordarguments are given a connection to localhost:9200 is established

        :param es_host: the Elasticsearch host
        :param es_port: the Elasticsearch port
        :param es_hosts: a list of dicts containing the Elasticsearch hosts to connect to
                         refer to https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch
                         for more information
        """
        self.ges = GdeltEs(es_host=es_host, es_port=es_port, es_hosts=es_hosts)

    def _get_default_payload(self):
        """
        Returns the default parameters used for the query, which is GeoJSON format and GDELT's PointData mode,
        which yields the following information for each feature:
        ['count', 'geometry', 'html', 'name', 'shareimage'].

        :return: (dict of str: str)
        """
        return {
            "format": "GeoJSON",
            "mode": "PointData",
        }

    def get_all_cities(self):
        """
        Retrieves the data for all four targeted cities of the CUTLER project

        :return:
        """
        for city, properties in cities.items():
            self.get_by_geolocation(properties['lat'], properties['long'], 20)

    def get_by_geolocation(self, lat, long, distance, imperial=True):
        """
        Retrieves the data for a given geolocation and within a given distance.
        The unit, in which the distance is measured, defaults to miles but can be changed to kilometers via the imperial
        kwarg.
        The result is retrieved in GeoJSON format and via GDELT's PointData mode, which yields the following
        information for each feature:
        ['count', 'geometry', 'html', 'name', 'shareimage'].

        :param lat: float the latitude of the geolocation
        :param long: float the longtitude of the geolocation
        :param distance: float the distance around the geolocation - defaults to miles
        :param imperial: bool True if miles should be used,
                              False if kilometers should be used
        :return:
        """
        payload = self._get_default_payload()
        payload['query'] = "near:" + ",".join(map(str, [lat, long, distance]))
        if not imperial:
            payload['query'] += "km"
        r = requests.get(self._base_url, params=payload)
        self.ges.index(r.json(), 'gdelt', 'doc')

    def get_by_location(self, location=None, locationadm1=None):
        """
        Retrieves the data for a specified location. The location can be specified by name or the first order
        administrative division (ADM1) as is used in the GDELT project.
        When both are given, the ADM1 code is favored as it returns a broader result.
        The result is retrieved in GeoJSON format and via GDELT's PointData mode, which yields the following
        information for each feature:
        ['count', 'geometry', 'html', 'name', 'shareimage'].

        See https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ for additional information.

        :param location: The location, which should be queried
        :param locationadm1: The ADM1 code of the location, which should be queried for
                             See http://data.gdeltproject.org/api/v2/guides/LOOKUP-ADM1S.TXT for the used ADM1 codes.
        :return:
        """
        payload = self._get_default_payload()
        if locationadm1 is not None:
            payload['query'] = "locationadm1:{}".format(locationadm1)
        else:
            if location is not None:
                payload['query'] = "location:\"{}\"".format(location)
        r = requests.get(self._base_url, params=payload)
        self.ges.index(r.json(), 'gdelt', 'doc')

    def get_by_keyword(self, keyword):
        """
        Retrieves the data for a specified keyword.
        See https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ for additional information.
        The result is retrieved in GeoJSON format and via GDELT's PointData mode, which yields the following
        information for each feature:
        ['count', 'geometry', 'html', 'name', 'shareimage'].

        :param keyword: The query string as is specified in https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/.
        :return:
        """
        payload = self._get_default_payload()
        if keyword is not None:
            payload['query'] = keyword
        else:
            return
        r = requests.get(self._base_url, params=payload)
        self.ges.index(r.json(), 'gdelt', 'doc')


if __name__ == '__main__':
    gc = GeoApiCrawler()
    gc.get_all_cities()
