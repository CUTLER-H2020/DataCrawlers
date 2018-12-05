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