"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The main functions gets data in SDMX json format from selected eurostat url and OECD
and creates python dictionaries with all the observations.
"""
from eurostat_functions import *
import time

if __name__ == "__main__":

    print("Downloading data from Eurostat")

    '''
    Eurostat - No. 1
    Population density by NUTS 3 region
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_d3dens&lang=en
    3 dimensions: "unit", "geo", "time"
    '''
    print('Eurostat - NO: 1 - 3 DIMs')
    demo_r_d3dens_dict = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/demo_r_d3dens?geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&geo=IE01&geo=IE011&geo=IE012&geo=IE013&geo=IE02&geo=IE021&geo=IE022&geo=IE023&geo=IE024&geo=IE025&geo=TR&geo=TR1&geo=TR10&geo=TR100&geo=TR2&geo=TR21&geo=TR211&geo=TR212&geo=TR213&geo=TR22&geo=TR221&geo=TR222&geo=TR3&geo=TR31&geo=TR310&geo=TR32&geo=TR321&geo=TR322&geo=TR323&geo=TR33&geo=TR331&geo=TR332&geo=TR333&geo=TR334&geo=TR4&geo=TR41&geo=TR411&geo=TR412&geo=TR413&geo=TR42&geo=TR421&geo=TR422&geo=TR423&geo=TR424&geo=TR425&geo=TR5&geo=TR51&geo=TR510&geo=TR52&geo=TR521&geo=TR522&geo=TR6&geo=TR61&geo=TR611&geo=TR612&geo=TR613&geo=TR62&geo=TR621&geo=TR622&geo=TR63&geo=TR631&geo=TR632&geo=TR633&geo=TR7&geo=TR71&geo=TR711&geo=TR712&geo=TR713&geo=TR714&geo=TR715&geo=TR72&geo=TR721&geo=TR722&geo=TR723&geo=TR8&geo=TR81&geo=TR811&geo=TR812&geo=TR813&geo=TR82&geo=TR821&geo=TR822&geo=TR823&geo=TR83&geo=TR831&geo=TR832&geo=TR833&geo=TR834&geo=TR9&geo=TR90&geo=TR901&geo=TR902&geo=TR903&geo=TR904&geo=TR905&geo=TR906&unit=HAB_KM2&precision=2",
        "unit", "geo", "time")
    print("FOUND: " + str(len(demo_r_d3dens_dict)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 2
    Population: Structure indicators by NUTS 3 region
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_pjanind3&lang=en
    4 dimensions: "indic_de","unit","geo","time"
    '''
    print('Eurostat - NO: 2 - 4 DIMs')
    demo_r_pjanind3 = parseeurostat4dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/demo_r_pjanind3?indic_de=DEPRATIO1&indic_de=DEPRATIO2&indic_de=FMEDAGEPOP&indic_de=MEDAGEPOP&indic_de=MMEDAGEPOP&indic_de=OLDDEP1&indic_de=OLDDEP2&indic_de=PC_FM&indic_de=PC_Y0_14&indic_de=PC_Y0_19&indic_de=PC_Y0_4&indic_de=PC_Y10_14&indic_de=PC_Y15_19&indic_de=PC_Y15_24&indic_de=PC_Y20_24&indic_de=PC_Y20_39&indic_de=PC_Y25_29&indic_de=PC_Y25_44&indic_de=PC_Y25_49&indic_de=PC_Y30_34&indic_de=PC_Y35_39&indic_de=PC_Y40_44&indic_de=PC_Y40_59&indic_de=PC_Y45_49&indic_de=PC_Y45_64&indic_de=PC_Y50_54&indic_de=PC_Y50_64&indic_de=PC_Y55_59&indic_de=PC_Y5_9&indic_de=PC_Y60_64&indic_de=PC_Y60_79&indic_de=PC_Y60_MAX&indic_de=PC_Y65_69&indic_de=PC_Y65_79&indic_de=PC_Y65_MAX&indic_de=PC_Y70_74&indic_de=PC_Y75_79&indic_de=PC_Y80_84&indic_de=PC_Y80_MAX&indic_de=PC_Y85_MAX&indic_de=YOUNGDEP1&indic_de=YOUNGDEP2&precision=2&geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&geo=IE01&geo=IE011&geo=IE012&geo=IE013&geo=IE02&geo=IE021&geo=IE022&geo=IE023&geo=IE024&geo=IE025&geo=TR&geo=TR1&geo=TR10&geo=TR100&geo=TR2&geo=TR21&geo=TR211&geo=TR212&geo=TR213&geo=TR22&geo=TR221&geo=TR222&geo=TR3&geo=TR31&geo=TR310&geo=TR32&geo=TR321&geo=TR322&geo=TR323&geo=TR33&geo=TR331&geo=TR332&geo=TR333&geo=TR334&geo=TR4&geo=TR41&geo=TR411&geo=TR412&geo=TR413&geo=TR42&geo=TR421&geo=TR422&geo=TR423&geo=TR424&geo=TR425&geo=TR5&geo=TR51&geo=TR510&geo=TR52&geo=TR521&geo=TR522&geo=TR6&geo=TR61&geo=TR611&geo=TR612&geo=TR613&geo=TR62&geo=TR621&geo=TR622&geo=TR63&geo=TR631&geo=TR632&geo=TR633&geo=TR7&geo=TR71&geo=TR711&geo=TR712&geo=TR713&geo=TR714&geo=TR715&geo=TR72&geo=TR721&geo=TR722&geo=TR723&geo=TR8&geo=TR81&geo=TR811&geo=TR812&geo=TR813&geo=TR82&geo=TR821&geo=TR822&geo=TR823&geo=TR83&geo=TR831&geo=TR832&geo=TR833&geo=TR834&geo=TR9&geo=TR90&geo=TR901&geo=TR902&geo=TR903&geo=TR904&geo=TR905&geo=TR906&unit=YR&unit=PC",
        "indic_de", "unit", "geo", "time")
    print("FOUND: " + str(len(demo_r_pjanind3)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 3
    Average annual population to calculate regional GDP data (thousand persons) by NUTS 3 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_3popgdp&lang=en
    3 dimensions: "unit", "geo", "time"
    '''
    print('Eurostat - NO: 3 - 3 DIMs')
    nama_10r_3popgdp = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_3popgdp?geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&unit=THS&precision=2",
        "unit", "geo", "time")
    print("FOUND: " + str(len(nama_10r_3popgdp)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 4
    Gross domestic product (GDP) at current market prices by NUTS 3 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_3gdp&lang=en
    3 dimensions: "unit", "geo", "time"
    '''
    print('Eurostat - NO: 4 - 3 DIMs')
    nama_10r_3gdp = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_3gdp?geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&unit=EUR_HAB&unit=EUR_HAB_EU&unit=MIO_EUR&unit=MIO_PPS&unit=PPS_HAB&unit=PPS_HAB_EU&precision=2",
        "unit", "geo", "time")
    print("FOUND: " + str(len(nama_10r_3gdp)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 5
    Gross value added at basic prices by NUTS 3 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_3gva&lang=en
    4 dimensions: "currency","nace_r2","geo","time"
    '''
    print('Eurostat - NO: 5 - 4 DIMs')
    nama_10r_3gva = parseeurostat4dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_3gva?precision=2&geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&geo=TR&geo=TR100&geo=TR211&geo=TR212&geo=TR213&geo=TR221&geo=TR222&geo=TR310&geo=TR321&geo=TR322&geo=TR323&geo=TR331&geo=TR332&geo=TR333&geo=TR334&geo=TR411&geo=TR412&geo=TR413&geo=TR421&geo=TR422&geo=TR423&geo=TR424&geo=TR425&geo=TR510&geo=TR521&geo=TR522&geo=TR611&geo=TR612&geo=TR613&geo=TR621&geo=TR622&geo=TR631&geo=TR632&geo=TR633&geo=TR711&geo=TR712&geo=TR713&geo=TR714&geo=TR715&geo=TR721&geo=TR722&geo=TR723&geo=TR811&geo=TR812&geo=TR813&geo=TR821&geo=TR822&geo=TR823&geo=TR831&geo=TR832&geo=TR833&geo=TR834&geo=TR901&geo=TR902&geo=TR903&geo=TR904&geo=TR905&geo=TR906&currency=MIO_EUR&nace_r2=A&nace_r2=B-E&nace_r2=C&nace_r2=F&nace_r2=G-I&nace_r2=G-J&nace_r2=J&nace_r2=K&nace_r2=K-N&nace_r2=L&nace_r2=M_N&nace_r2=O-Q&nace_r2=O-U&nace_r2=R-U&nace_r2=TOTAL",
        "currency", "nace_r2", "geo", "time")
    print("FOUND: " + str(len(nama_10r_3gva)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 6
    Employment (thousand persons) by NUTS 3 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_3empers&lang=en
    5 dimensions: "unit","wstatus","nace_r2","geo","time" 
    '''
    print('Eurostat - NO: 6 - 5 DIMs')
    nama_10r_3empers = parseeurostat5dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_3empers?precision=2&geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL3&geo=EL30&geo=EL301&geo=EL302&geo=EL303&geo=EL304&geo=EL305&geo=EL306&geo=EL307&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=EL5&geo=EL51&geo=EL511&geo=EL512&geo=EL513&geo=EL514&geo=EL515&geo=EL52&geo=EL521&geo=EL522&geo=EL523&geo=EL524&geo=EL525&geo=EL526&geo=EL527&geo=EL53&geo=EL531&geo=EL532&geo=EL533&geo=EL54&geo=EL541&geo=EL542&geo=EL543&geo=EL6&geo=EL61&geo=EL611&geo=EL612&geo=EL613&geo=EL62&geo=EL621&geo=EL622&geo=EL623&geo=EL624&geo=EL63&geo=EL631&geo=EL632&geo=EL633&geo=EL64&geo=EL641&geo=EL642&geo=EL643&geo=EL644&geo=EL645&geo=EL65&geo=EL651&geo=EL652&geo=EL653&geo=IE&geo=IE0&geo=IE01&geo=IE011&geo=IE012&geo=IE013&geo=IE02&geo=IE021&geo=IE022&geo=IE023&geo=IE024&geo=IE025&unit=THS&wstatus=EMP&wstatus=SAL&nace_r2=A&nace_r2=B-E&nace_r2=C&nace_r2=F&nace_r2=G-I&nace_r2=G-J&nace_r2=J&nace_r2=K&nace_r2=K-N&nace_r2=L&nace_r2=M_N&nace_r2=O-Q&nace_r2=O-U&nace_r2=R-U&nace_r2=TOTAL",
        "unit", "wstatus", "nace_r2", "geo", "time")
    print("FOUND: " + str(len(nama_10r_3empers)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 7
    Income of households by NUTS 2 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_2hhinc&lang=en
    4 dimensions: "unit","na_item","geo","time" 
    '''
    print('Eurostat - NO: 7 - 4 DIMs')
    nama_10r_2hhinc = parseeurostat4dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_2hhinc?na_item=B5N&na_item=B6N&precision=2&geo=BE&geo=BE1&geo=BE10&geo=BE2&geo=BE21&geo=BE22&geo=BE23&geo=BE24&geo=BE25&geo=BE3&geo=BE31&geo=BE32&geo=BE33&geo=BE34&geo=BE35&geo=EL&geo=EL3&geo=EL30&geo=EL4&geo=EL41&geo=EL42&geo=EL43&geo=EL5&geo=EL51&geo=EL52&geo=EL53&geo=EL54&geo=EL6&geo=EL61&geo=EL62&geo=EL63&geo=EL64&geo=EL65&geo=IE&geo=IE0&geo=IE01&geo=IE02&geo=TR&geo=TR1&geo=TR10&geo=TR2&geo=TR21&geo=TR22&geo=TR3&geo=TR31&geo=TR32&geo=TR33&geo=TR4&geo=TR41&geo=TR42&geo=TR5&geo=TR51&geo=TR52&geo=TR6&geo=TR61&geo=TR62&geo=TR63&geo=TR7&geo=TR71&geo=TR72&geo=TR8&geo=TR81&geo=TR82&geo=TR83&geo=TR9&geo=TR90&unit=EUR_HAB&unit=MIO_EUR&unit=MIO_NAC&unit=MIO_PPCS&unit=PPCS_HAB&unit=PPCS_HAB_EU",
        "unit", "na_item", "geo", "time")
    print("FOUND: " + str(len(nama_10r_2hhinc)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 8
    Secondary distribution of income account of households by NUTS 2 regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10r_2hhsec&lang=en
    5 dimensions: "unit","direct","na_item","geo","time" 
    '''
    print('Eurostat - NO: 8 - 5 DIMs')
    nama_10r_2hhsec = parseeurostat5dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10r_2hhsec?na_item=B6N&na_item=D5&na_item=D61&na_item=D7&na_item=D62&precision=2&direct=BAL&direct=PAID&direct=RECV&geo=BE&geo=BE1&geo=BE10&geo=BE2&geo=BE21&geo=BE22&geo=BE23&geo=BE24&geo=BE25&geo=BE3&geo=BE31&geo=BE32&geo=BE33&geo=BE34&geo=BE35&geo=BEZ&geo=BEZZ&geo=EL&geo=EL3&geo=EL30&geo=EL4&geo=EL41&geo=EL42&geo=EL43&geo=EL5&geo=EL51&geo=EL52&geo=EL53&geo=EL54&geo=EL6&geo=EL61&geo=EL62&geo=EL63&geo=EL64&geo=EL65&geo=IE&geo=IE0&geo=IE01&geo=IE02&geo=IEZ&geo=IEZZ&unit=MIO_EUR",
        "unit", "direct", "na_item", "geo", "time")
    print("FOUND: " + str(len(nama_10r_2hhsec)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 9
    Number of establishments, bedrooms and bed-places by NUTS 3 regions (1990-2011)
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_cap_nuts3&lang=en
    5 dimensions: "accommod","unit","nace_r2","geo","time"
    '''
    print('Eurostat - NO: 9 - 5 DIMs')
    tour_cap_nuts3 = parseeurostat5dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tour_cap_nuts3?precision=2&geo=BE&geo=BE1&geo=BE10&geo=BE100&geo=BE2&geo=BE21&geo=BE211&geo=BE212&geo=BE213&geo=BE22&geo=BE221&geo=BE222&geo=BE223&geo=BE23&geo=BE231&geo=BE232&geo=BE233&geo=BE234&geo=BE235&geo=BE236&geo=BE24&geo=BE241&geo=BE242&geo=BE25&geo=BE251&geo=BE252&geo=BE253&geo=BE254&geo=BE255&geo=BE256&geo=BE257&geo=BE258&geo=BE3&geo=BE31&geo=BE310&geo=BE32&geo=BE321&geo=BE322&geo=BE323&geo=BE324&geo=BE325&geo=BE326&geo=BE327&geo=BE33&geo=BE331&geo=BE332&geo=BE334&geo=BE335&geo=BE336&geo=BE34&geo=BE341&geo=BE342&geo=BE343&geo=BE344&geo=BE345&geo=BE35&geo=BE351&geo=BE352&geo=BE353&geo=EL&geo=EL1&geo=EL11&geo=EL111&geo=EL112&geo=EL113&geo=EL114&geo=EL115&geo=EL12&geo=EL121&geo=EL122&geo=EL123&geo=EL124&geo=EL125&geo=EL126&geo=EL127&geo=EL13&geo=EL131&geo=EL132&geo=EL133&geo=EL134&geo=EL14&geo=EL141&geo=EL142&geo=EL143&geo=EL144&geo=EL2&geo=EL21&geo=EL211&geo=EL212&geo=EL213&geo=EL214&geo=EL22&geo=EL221&geo=EL222&geo=EL223&geo=EL224&geo=EL23&geo=EL231&geo=EL232&geo=EL233&geo=EL24&geo=EL241&geo=EL242&geo=EL243&geo=EL244&geo=EL245&geo=EL25&geo=EL251&geo=EL252&geo=EL253&geo=EL254&geo=EL255&geo=EL3&geo=EL30&geo=EL300&geo=EL4&geo=EL41&geo=EL411&geo=EL412&geo=EL413&geo=EL42&geo=EL421&geo=EL422&geo=EL43&geo=EL431&geo=EL432&geo=EL433&geo=EL434&geo=IE&geo=IE0&geo=IE01&geo=IE011&geo=IE012&geo=IE013&geo=IE02&geo=IE021&geo=IE022&geo=IE023&geo=IE024&geo=IE025&geo=TR&geo=TR1&geo=TR10&geo=TR100&geo=TR2&geo=TR21&geo=TR211&geo=TR212&geo=TR213&geo=TR22&geo=TR221&geo=TR222&geo=TR3&geo=TR31&geo=TR310&geo=TR32&geo=TR321&geo=TR322&geo=TR323&geo=TR33&geo=TR331&geo=TR332&geo=TR333&geo=TR334&geo=TR4&geo=TR41&geo=TR411&geo=TR412&geo=TR413&geo=TR42&geo=TR421&geo=TR422&geo=TR423&geo=TR424&geo=TR425&geo=TR5&geo=TR51&geo=TR510&geo=TR52&geo=TR521&geo=TR522&geo=TR6&geo=TR61&geo=TR611&geo=TR612&geo=TR613&geo=TR62&geo=TR621&geo=TR622&geo=TR63&geo=TR631&geo=TR632&geo=TR633&geo=TR7&geo=TR71&geo=TR711&geo=TR712&geo=TR713&geo=TR714&geo=TR715&geo=TR72&geo=TR721&geo=TR722&geo=TR723&geo=TR8&geo=TR81&geo=TR811&geo=TR812&geo=TR813&geo=TR82&geo=TR821&geo=TR822&geo=TR823&geo=TR83&geo=TR831&geo=TR832&geo=TR833&geo=TR834&geo=TR9&geo=TR90&geo=TR901&geo=TR902&geo=TR903&geo=TR904&geo=TR905&geo=TR906&unit=NR&accommod=BEDPL&accommod=BEDRM&accommod=ESTBL&nace_r2=I551&nace_r2=I551-I553&nace_r2=I552&nace_r2=I552_I553&nace_r2=I553",
        "accommod", "unit", "nace_r2", "geo", "time")
    print("FOUND: " + str(len(tour_cap_nuts3)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 10
    Employment by NACE Rev. 2 activity and metropolitan typology
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=met_10r_3emp&lang=en
    5 dimensions: "unit","wstatus","nace_r2","metroreg","time"
    '''
    print('Eurostat - NO: 10 - 5 DIMs')
    met_10r_3emp = parseeurostat5dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/met_10r_3emp?precision=2&unit=THS_PER&metroreg=BE&metroreg=BE001MC&metroreg=BE002M&metroreg=BE003M&metroreg=BE004M&metroreg=BE005M&metroreg=BE_NM&metroreg=EL&metroreg=EL001MC&metroreg=EL002M&metroreg=EL_NM&metroreg=IE&metroreg=IE001MC&metroreg=IE002M&metroreg=IE_NM&wstatus=EMP&wstatus=SAL&nace_r2=A&nace_r2=B-E&nace_r2=C&nace_r2=F&nace_r2=G-I&nace_r2=G-J&nace_r2=J&nace_r2=K&nace_r2=K-N&nace_r2=L&nace_r2=M_N&nace_r2=O-Q&nace_r2=O-U&nace_r2=R-U&nace_r2=TOTAL",
        "unit", "wstatus", "nace_r2", "metroreg", "time")
    print("FOUND: " + str(len(met_10r_3emp)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 11
    Gross domestic product (GDP) at current market prices by metropolitan regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=met_10r_3gdp&lang=en
    3 dimensions: "unit","metroreg","time"
    '''
    print('Eurostat - NO: 11 - 3 DIMs')
    met_10r_3gdp = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/met_10r_3gdp?precision=2&unit=EUR_HAB_EU&unit=MIO_EUR&unit=MIO_PPS&unit=PPS_HAB&unit=PPS_HAB_EU&metroreg=BE001MC&metroreg=BE002M&metroreg=BE003M&metroreg=BE004M&metroreg=BE005M&metroreg=BE_NM&metroreg=EL001MC&metroreg=EL002M&metroreg=EL_NM&metroreg=IE001MC&metroreg=IE002M&metroreg=IE_NM",
        "unit", "metroreg", "time")
    print("FOUND: " + str(len(met_10r_3gdp)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 12
    Economically active population by sex, age and metropolitan regions
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=met_lfp3pop&lang=en
    5 dimensions: "unit","age","sex","metroreg","time"
    '''
    print('Eurostat - NO: 12 - 3 DIMs')
    met_lfp3pop = parseeurostat5dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/met_lfp3pop?precision=2&sex=F&sex=M&sex=T&unit=THS_PER&metroreg=BE001MC&metroreg=BE002M&metroreg=BE003M&metroreg=BE004M&metroreg=BE005M&metroreg=BE_NM&metroreg=EL001MC&metroreg=EL002M&metroreg=EL_NM&metroreg=IE001MC&metroreg=IE002M&metroreg=IE_NM&age=Y15-24&age=Y15-74&age=Y20-64&age=Y_GE15&age=Y_GE25",
        "unit", "age", "sex", "metroreg", "time")
    print("FOUND: " + str(len(met_lfp3pop)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 13
    Economy and finance - cities and greater cities
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=urb_cecfi&lang=en
    3 dimensions: "indic_ur","cities","time"
    '''
    print('Eurostat - NO: 13 - 3 DIMs')
    urb_cecfi = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/urb_cecfi?indic_ur=EC2021V&indic_ur=EC2039V&cities=BE&cities=BE001C1&cities=BE002C1&cities=BE003C1&cities=BE004C1&cities=BE005C1&cities=BE006C1&cities=BE007C1&cities=BE008C1&cities=BE009C1&cities=BE010C1&cities=BE011C1&cities=EL&cities=EL001C1&cities=EL001K1&cities=EL002C1&cities=EL003C1&cities=EL004C1&cities=EL005C1&cities=EL006C1&cities=EL007C1&cities=EL008C1&cities=EL009C1&cities=TR001C1&cities=TR002C1&cities=TR003C1&cities=TR004C1&cities=TR005C1&cities=TR006C1&cities=TR007C1&cities=TR008C1&cities=TR009C1&cities=TR010C1&cities=TR011C1&cities=TR012C1&cities=TR013C1&cities=TR014C1&cities=TR015C1&cities=TR016C1&cities=TR017C1&cities=TR018C1&cities=TR019C1&cities=TR020C1&cities=TR021C1&cities=TR022C1&cities=TR023C1&cities=TR024C1&cities=TR025C1&cities=TR026C1&precision=2",
        "indic_ur", "cities", "time")
    print("FOUND: " + str(len(urb_cecfi)) + " observations")
    time.sleep(5)

    '''
    Eurostat - No. 14
    Culture and tourism - cities and greater cities
    URL: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=urb_ctour&lang=en
    3 dimensions: "indic_ur","cities","time"
    '''
    print('Eurostat - NO: 14 - 3 DIMs')
    urb_ctour = parseeurostat3dimensions(
        "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/urb_ctour?indic_ur=CR1003I&indic_ur=CR1003V&indic_ur=CR1005V&indic_ur=CR1007V&indic_ur=CR1008V&indic_ur=CR1010V&indic_ur=CR1015V&indic_ur=CR2001V&indic_ur=CR2009V&indic_ur=CR2010I&indic_ur=CR2011I&cities=BE&cities=BE001C1&cities=BE002C1&cities=BE003C1&cities=BE004C1&cities=BE005C1&cities=BE006C1&cities=BE007C1&cities=BE008C1&cities=BE009C1&cities=BE010C1&cities=BE011C1&cities=EL&cities=EL001C1&cities=EL002C1&cities=EL003C1&cities=EL004C1&cities=EL005C1&cities=EL006C1&cities=EL007C1&cities=EL008C1&cities=EL009C1&cities=IE&cities=IE001C1&cities=IE002C1&cities=IE003C1&cities=IE004C1&cities=IE005C1&cities=TR001C1&cities=TR002C1&cities=TR003C1&cities=TR004C1&cities=TR005C1&cities=TR006C1&cities=TR007C1&cities=TR008C1&cities=TR009C1&cities=TR010C1&cities=TR011C1&cities=TR012C1&cities=TR013C1&cities=TR014C1&cities=TR015C1&cities=TR016C1&cities=TR017C1&cities=TR018C1&cities=TR019C1&cities=TR020C1&cities=TR021C1&cities=TR022C1&cities=TR023C1&cities=TR024C1&cities=TR025C1&cities=TR026C1&precision=2",
        "indic_ur", "cities", "time")
    print("FOUND: " + str(len(urb_ctour)) + " observations")
    time.sleep(5)
