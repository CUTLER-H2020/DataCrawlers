# Crawler for Eurostat

DUTH's crawler to download data from Eurostat
The crawler downloads data for several economic indicators from Eurostat for the 4 pilot-cities and their regions (Antalya, Antwerp, Cork, Thessaloniki)
The table bellow presents both the economic indicators and the fields used by the crawler:

| Dataset  | Fields |
| ------------- | ------------- |
| Population density by NUTS 3 region  | "unit", "geo", "time"  |
| Population: Structure indicators by NUTS 3 region  | "indic_de","unit","geo","time"  |
| Average annual population to calculate regional GDP data (thousand persons) by NUTS 3 regions  | "unit", "geo", "time"  |
| Gross domestic product (GDP) at current market prices by NUTS 3 regions  | "unit", "geo", "time"  |
| Gross value added at basic prices by NUTS 3 regions  | "currency", "nace_r2", "geo", "time"  |
| Employment (thousand persons) by NUTS 3 regions  | "unit","wstatus","nace_r2","geo","time"   |
| Income of households by NUTS 2 regions  | "unit", "na_item", "geo", "time"  |
| Secondary distribution of income account of households by NUTS 2 regions  | "unit","direct","na_item","geo","time"  |
| Number of establishments, bedrooms and bed-places by NUTS 3 regions (1990-2011)  | "accommod","unit","nace_r2","geo","time"  |
| Employment by NACE Rev. 2 activity and metropolitan typology  | "unit","wstatus","nace_r2","metroreg","time"  |
| Gross domestic product (GDP) at current market prices by metropolitan regions  | "unit","metroreg","time"  |
| Economically active population by sex, age and metropolitan regions  | "unit","age","sex","metroreg","time"  |
| Economy and finance - cities and greater cities  | "indic_ur","cities","time"  |
| Culture and tourism - cities and greater cities  | "indic_ur","cities","time"  |

The table bellow describes the fields used by the crawler

| Field  | Description |
| ------------- | ------------- |
| geo  | geopolitical entity  |
| time  | period of time  |
| unit  | unit of measure  |
| indic_de  | Demographic indicator  |
| currency  | currency  |
| nace_r2  | classification of economic activities  |
| wstatus  | activity and employment status  |
| na_item  | national accounts indicator (ESA 2010)  |
| accommod  | Mode of accomodation  |
| metroreg  | metropolitan regions  |
| age  | age  |
| sex  | sex  |
| cities  | geopolitical entity (declaring)  |
| indic_ur  | urban audit indicator  |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. The crawler downloads the data from Eurostat and saves them in JSON files.

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Install python3 - virtualenv
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
```

### Installing

1. Create a new virtual enviroment
```
$ virtualenv -p python3 myenv
$ source myenv/bin/activate
```

2. Run the crawler
```
(myenv) $ python3 main.py
```
