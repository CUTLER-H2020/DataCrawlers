from elasticsearch import Elasticsearch


class ElasticSearchClient:
    def __init__(self, host: str, port: str, use_ssl, verify_certs, http_auth, ca_certs):
        self.es = Elasticsearch(['{}:{}'.format(host, port)],
                                use_ssl=use_ssl,
                                verify_certs=verify_certs,
                                http_auth=http_auth,
                                ca_certs=ca_certs)

        self.index = None

    def insert_doc(self, doc_: dict, id_: str = None) -> str:
        res = self.es.index(index=self.index, body=doc_, id=id_)
        return res['result']

    @staticmethod
    def define_geo_point_mapping():
        geo_mapping = {
            "mappings": {
                "properties": {
                    "location": {
                        "type": "geo_point"
                    }
                }
            }

        }
        return geo_mapping

    @staticmethod
    def define_custom_geo_point_mapping(geo_point_field_name):
        geo_mapping = {
            "mappings": {
                "properties": {
                    geo_point_field_name: {
                        "type": "geo_point"
                    }
                }
            }

        }
        return geo_mapping

    @staticmethod
    def define_date_mapping():
        date_mapping = {
            "mappings": {
                "properties": {
                    "Date": {
                        "type": "date",
                        # This is a built-in format of Elasticsearch. Check:
                        # https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats
                        "format": "date_optional_time"
                    }
                }
            }
        }
        return date_mapping

    @staticmethod
    def define_custom_date_mapping_format(date_field_name, format):
        date_mapping = {
            "mappings": {
                "properties": {
                    date_field_name: {
                        "type": "date",
                        # This is a built-in format of Elasticsearch. Check:
                        # https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats
                        "format": format
                    }
                }
            }
        }
        return date_mapping

    def create_index(self, index: str, *mappings):

        self.index = index

        unified_mapping = {
            "mappings": {
                "properties": {}
            }
        }

        for mapping in mappings:
            unified_mapping['mappings']['properties'].update(mapping['mappings']['properties'])

        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body=unified_mapping)

