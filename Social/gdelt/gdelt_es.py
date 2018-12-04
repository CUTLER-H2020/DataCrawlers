from math import ceil

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime

import geopandas as gpd
import pandas as pd

class GdeltEs:
    """
    A helper class for indexing and accessing GDELT data in elasticsearch
    """

    def __init__(self, es_host=None, es_port=None, es_hosts=None):
        """
        Initialize the Wrapper and establish the Elasticsearch connection.
        If no Elasticsearch host or no elasticsearch host is given, a connection to Elasticsearch standard
        "localhost:9200/" is established.

        :param es_host: The Elasticsearch host
        :param es_port: The Elasticsearch port
        :param es_hosts: a list of dicts containing the Elasticsearch hosts to connect to
                         refer to https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch
                         for more information
        """
        if es_hosts is not None:
            self.es = Elasticsearch(es_hosts)
        else:
            if es_host is None or es_port is None:
                self.es = Elasticsearch()
            else:
                self.es = Elasticsearch([{'host': es_host, 'port': es_port}])

    def _get_documents(self, data):
        """

        Returns a well-formed dict of the documents with an added 'created' key-value pair, which indicates the current
        date and hence the date the data is indexed.

        :param data: The GeoJSON, which is returned by the GDELT GEO API
        :return: dict of the data containing an additional created key-value pair indicating, when the data was
                      indexed
        """
        gdf = gpd.GeoDataFrame(data)
        gdf['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gdf = gdf.reindex(sorted(gdf.columns), axis=1)
        return gdf.to_dict(orient='records')

    def count(self, index, doc_type, body=None):
        """
        Returns the count of data indexed under the given index.

        :param index: The index, for which the count shall be returned
        :param doc_type: The doc_type specified in the index mapping
        :param body: The body of the search query, see
                     https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
                     for reference.
                     If no body is given all results are matched.
        :return:
        """
        if body is None:
            body = {
                'query': {
                    'match_all': {}
                }
            }
     
        return self.es.count(index=index, doc_type=doc_type, body=body)['count']

    def index(self, data, index, doc_type):
        """
        Indexes the given data to the given elasticsearch index. The doc_type has to match the doc_type specified in the
        elasticsearch mapping defined upon index creation.

        :param data:     The GeoJSON, which is returned by the GDELT GEO API
        :param index:    The index, where the data shall be indexed
        :param doc_type: The doc_type specified in the index mapping
        :raises Exception when the operation fails. The exceptions are propagated from the underlying elasticsearch API
        :return:
        """
        documents = self._get_documents(data)
        bulk(self.es, documents, index=index, doc_type=doc_type, raise_on_error=True)

    def search(self, index, doc_type, body=None):
        """
        Returns the data indexed under the given index.

        :param index: The index, for which the data shall be returned
        :param doc_type: The doc_type specified in the index mapping
        :param body: The body of the search query, see
                     https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
                     for reference.
                     If no body is given all results are matched.
        :return:
        """

        # the result size can not be over 10000 for one request
        if body is None:
            body = {
                'size': 10000,
                'query': {
                    'match_all': {}
                }
            }

        return self.es.search(index=index, doc_type=doc_type, body=body, scroll='1m')

    def get_as_gdf(self, index, doc_type, body=None):
        """
        Returns the data indexed under the given index as a GeoPandas GeoDataFrame.

        :param index: The index, for which the data shall be returned
        :param doc_type: The doc_type specified in the index mapping
        :param body: The body of the search query, see
                     https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
                     for reference.
                     If no body is given all results are matched.
        :return:
        """
        data = self.search(index=index, doc_type=doc_type, body=body)

        frames = []
        for elem in data['hits']['hits']:
            frames.append(gpd.GeoDataFrame(elem['_source']))
        gdf = gpd.GeoDataFrame(pd.concat(frames))

        return gdf
