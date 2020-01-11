#!/usr/bin/env python3
def crawlReview(reviews):
    result = []
    for rev in reviews:
        tempTitle = rev.find_elements_by_class_name("location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT")
        if len(tempTitle) > 0:
            title = tempTitle[0].text
        else:
            title = ""
        tempUser = rev.find_elements_by_class_name("ui_header_link.social-member-event-MemberEventOnObjectBlock__member--35-jC")
        if len(tempUser) > 0:
            user = tempUser[0].text
        else:
            user = ""
        tempRating = rev.find_elements_by_class_name("ui_bubble_rating")
        if len(tempRating) > 0:
            rating = int(tempRating[0].get_attribute("class")[-2:])/10
        else:
            rating = -1
        tempHelpful = rev.find_elements_by_class_name("social-statistics-bar-SocialStatisticsBar__counts--3Zm4V.social-statistics-bar-SocialStatisticsBar__item--2IlT7")
        if (len(tempHelpful) > 0) and ("Helpful vote" in tempHelpful[0].text):
            helpful = int(tempHelpful[0].text[slice(0,-13,1)])
        else:
            helpful = 0
        tempComment = rev.find_elements_by_class_name("location-review-review-list-parts-ExpandableReview__reviewText--gOmRC")
        if len(tempComment) > 0:
            comment = tempComment[0].text
        else:
            comment = ""
        tempDate = rev.find_elements_by_class_name("location-review-review-list-parts-EventDate__event_date--1epHa")
        if len(tempDate) > 0:
            if hotel == True:
                date = tempDate[0].text[slice(14,None,1)]
            else:
                date = tempDate[0].text[slice(20,None,1)]
        else:
            date = ""
        #write into result
        entry = [ title.replace('"', '\"'), user.replace('"', '\"'), rating, helpful, comment.replace('"', '\"').replace('\n', ' '), date ]
        result.append(entry)
    return result

#Selenium WebDriver settings, refer to https://selenium.dev/documentation/en/webdriver/driver_requirements/
#and follow the instructions for your browser and OS
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as expected_conditions
import sys
import pandas as pd
import numpy as np

opt = Options()
opt.headless = True
driver = Firefox(options=opt)

global hotel
if (len(sys.argv) > 1) and (sys.argv[1] == "-h"):
    hotel = True
else:
    hotel = False

site_list = open("sites.txt")
for site in site_list:
    end = False
    entries = []
    #navigate to page and get location name
    driver.get(site)
    print("Crawling " + site)

    tempLocName = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_element_located((By.ID,"HEADING")))
    tempLocName = tempLocName.text
    locName = ""
    for char in tempLocName:
        if char == " ":
            locName = locName + "_"
        else:
            locName = locName + char
    fn = "comment_data_" + locName
    #crawl for reviews
    pn = 1
    print("Crawling Page 1", end="")
    more = WebDriverWait(driver, timeout=10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"location-review-review-list-parts-ExpandableReview__cta--2mR2g")))
    more.click()

    if hotel == True:
        revs = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"hotels-community-tab-common-Card__card--ihfZB.hotels-community-tab-common-Card__section--4r93H")))
    else:
        revs = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"location-review-card-Card__ui_card--2Mri0.location-review-card-Card__card--o3LVm.location-review-card-Card__section--NiAcw")))

    revsResult = crawlReview(revs)
    if len(entries) == 0:
        entries = revsResult
    else:
        entries = np.concatenate((entries, revsResult), axis=0)

    btn = driver.find_elements_by_class_name("ui_button.nav.next.primary")
    if len(btn) > 0:
        bt = WebDriverWait(driver, timeout=10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"ui_button.nav.next.primary")))
        bt.click()
    else:
        end = True

    while end == False:
        pn = pn + 1
        print("\rCrawling Page " + str(pn),end="")

        more = WebDriverWait(driver, timeout=10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"location-review-review-list-parts-ExpandableReview__cta--2mR2g")))
        more.click()

        if hotel == True:
            revs = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"hotels-community-tab-common-Card__card--ihfZB.hotels-community-tab-common-Card__section--4r93H")))
        else:
            revs = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"location-review-card-Card__ui_card--2Mri0.location-review-card-Card__card--o3LVm.location-review-card-Card__section--NiAcw")))
        revsResult = crawlReview(revs)
        if len(entries) == 0:
            entries = revsResult
        else:
            entries = np.concatenate((entries, revsResult), axis=0)

        if len(driver.find_elements_by_class_name("ui_button.nav.next.primary.disabled")) > 0:
            end = True
        else:
            btn = WebDriverWait(driver, timeout=10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"ui_button.nav.next.primary")))
            btn.click()

    print("\nSite crawled")

    # output file
    df = pd.DataFrame(np.array(entries))
    df.to_csv(fn, header=False, index=False)

driver.quit()
site_list.close()
