# Crawlers and Indexer for twitter

This folder contains different crawlers for the GDELT dataset. [GDELT](https://www.gdeltproject.org/) is a project, which monitors news from all over the world and in more than 100 languages in order to gather data about current events. As part of the project, events are indexed in a 15-minute timeframe and can be retrieved with different methods. The indexed data comprises features such as date, number of mentions, average sentiment and geolocations. A schema of the indexed data can be found in the [GDELT GitHub repository](https://github.com/linwoodc3/gdelt2HeaderRows/tree/master/schema_csvs).

For details please refer to [Deliverable 6.1](https://www.cutler-h2020.eu/download/538).

**Indexing GDELT GEO API data into Elasticsearch**

**1) Retrieve data from Geo API** 

Use GeoApiCrawler to retrieve data by keyword/location/geolocation or from all four cities in the CUTLER project.

**2) Create Elasticsearch index**

Go to Kibana-> Dev Tools-> Console and execute:

```
PUT /gdelt
{
  "mappings": {
    "doc": {
      "properties": {
        "features.geometry.coordinates": {
          "type": "geo_point"
        },
        "features.count.properties": {
          "type": "long"
        },
        "features.name.properties": {
          "type": "text"
        },
        "features.html.properties": {
          "type": "text"
        },
        "created" : {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss"
        }
      }
    }
  }
}
```

**3) Import data to Elasticsearch**

Use the index function in the GdeltEs class

**The last steps are the same as outlined in Step4 and Step5 in [cutler-es-imc](https://github.com/MKLab-ITI/cutler-es-imc)**
