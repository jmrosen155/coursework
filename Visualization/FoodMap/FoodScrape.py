# Created by Justin Law
# Date: 14/07/2014

import urllib2
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import json

# Load csv file containing restaurant urls.
# Also contains metadata such as name/id of restaurant, name of food item, category of food item, prices of food item, number of reviews of food item, link to reviews, link to photos
restaurantdata = pd.read_csv("restaurants_json.csv")

# Collect urls and change url of the business to its menu
url = list(restaurantdata.url)
for i in range(len(url)):
    url[i] = url[i].replace("biz","menu")
    
store = []
# num stores the number of urls that do not exist (number of restaurants that do not have menu page on Yelp)
num = 0
index = 0

# Scrape food items and its metadata
for i in range(len(restaurantdata)):
    try:
        page = urllib2.urlopen(url[i])
    except Exception, e:
        print e, restaurantdata.name[i]
        num += 1
        continue
    soup = bs(page)
    restaurant = restaurantdata.name[i]
    business_id = restaurantdata.business_id[i]

    for itemcategory in soup("div",class_="menu-section-header"):
        category = itemcategory.find("h2").contents[0].strip()
        for item in itemcategory.next_sibling.next_sibling("div",class_="menu-item"):
            fooditem = {}
            if item.find("div",class_="menu-item-details").find("a"):
                if item.find("div",class_="menu-item-details").find("a").contents[0].strip() != '':
                    name = item.find("div",class_="menu-item-details").find("a").contents[0].strip()
                else: 
                    name = item.find("div",class_="menu-item-details").find("h3").contents[0].strip()
            else:
                name = item.find("div",class_="menu-item-details").find("h3").contents[0].strip()
            if item.find("p"):
                description = item.find("p").contents[0].strip()
            else:
                description = ''
            if item.find("li",class_="menu-item-price-amount"):
                prices = item.find("li",class_="menu-item-price-amount").contents[0].strip()
            elif item.findAll("th",class_="menu-item-price-label"):
                prices = []
                pricelabels = item.findAll("th",class_="menu-item-price-label")
                priceamounts = item.findAll("td",class_="menu-item-price-amount")
                for i in range(len(pricelabels)):
                    prices.append(pricelabels[i].contents[0].strip() + ': ' + str(priceamounts[0].contents[0].strip()))
            else:
                prices = None
            if item.find("a",class_="num-reviews"):
                review_num = int(re.sub("[A-Za-z]","",item.find("a", class_="num-reviews").next_element.next_element).strip())
                review_url = item.find("a",class_="num-reviews").get('href')
            else:
                review_num = 0
                review_url = ''
            if item.find("a", class_="i-grey-camera-menus-wrap"):
                photo_num = int(re.sub("[A-Za-z]","",item.find("a", class_="i-grey-camera-menus-wrap").next_element.next_element).strip())
                photo_url = item.find("a", class_="i-grey-camera-menus-wrap").get('href')
            else:
                photo_num = 0
                photo_url = ''

            fooditem["restaurant"] = restaurant
            fooditem["business_id"] = business_id
            fooditem["category"] = category
            fooditem["name"] = name
            fooditem["prices"] = prices
            fooditem["description"] = description
            fooditem["review_num"] = review_num
            fooditem["review_url"] = review_url
            fooditem["photo_num"] = photo_num
            fooditem["photo_url"] = photo_url
            fooditem["foodkey"] = index

            index += 1
            store.append(fooditem)

foodFrame = pd.DataFrame(store)

# Scrape urls of photos given the photo url of each food item previously scraped
photos = []
photourls = foodFrame[foodFrame.photo_url != ''][['foodkey', 'photo_url']] 

photostore = []
for i in range(len(photourls)):
    weburl = "http://www.yelp.com/" + photourls.iloc[i].photo_url
    photopage = urllib2.urlopen(weburl)
    photosoup = bs(photopage)
    foodkey = photourls.iloc[i].foodkey

    # There are several photos under class pb-180s, just pick the first one
    photo = photosoup(class_="pb-180s")[0]
    photoitem = {}
    photoitem["foodkey"] = foodkey
    photoitem["src"] = photo.find("img").get("src")
    photostore.append(photoitem)

photoFrame = pd.DataFrame(photostore)

photoFrame.to_csv("photoFrame.csv", encoding="utf-8")

# Joining the photo information with the food metadata
index_food = foodFrame.set_index('foodkey')
index_photo = photoFrame.set_index('foodkey')
photojoin = index_food.join(index_photo, how='inner')

# Filtering for photos that has reviews
photorem = photojoin[photojoin.review_num > 0]


# Additional scraping for price range of restaurants
url = list(restaurantdata.url)
  
rststore = []
num = 0
for i in range(len(url)):
    rstitem = {}
    try:
        page = urllib2.urlopen(url[i])
    except Exception, e:
        print e, restaurantdata.name[i]
        num += 1
        continue
    soup = bs(page)
    if soup("span", class_="price-range"):
        rstitem["pricerange"] = soup("span", class_="price-range")[0].contents[0].encode('ascii','ignore')
        rstitem["business_id"] = restaurantdata.business_id[i]
        rststore.append(rstitem)

priceFrame = pd.DataFrame(rststore)