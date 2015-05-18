---
title: "Yelp Data 2D Search Clean"
author: "Sam Guleff"
date: "Thursday, April 20, 2015"
output: html_document
layout: post
description: Final Project
tags: assignments Sam Guleff R Sample Code, Presentaiton
---

#Yelp 2D Preference Searching by Cuisine

When searching for restaurants we tend to compare price and ratings but there's no quick and easy way to see both.
Woulden't it be great to plot these at the same time so we can weight them against each other before making a choice.
Additionally our tolarence for cost and ratings isn't the same for all cuisines.  Can we use this additional info to 
make a better choice?


#####Since the data provided is in 1/2 star and integer ratings we will need to jitter them.
#####In production we would use actual values.
```

#function to jitter the samples
jitterSamples <- function(sample){
  for (i in 0: nrow(sample) - 1 ) 
  {
    sample[i,1] = sample[i,1] + runif(1, -.1, .1)
    sample[i,2] = sample[i,2] + runif(1, -.1, .1)
  }
  return(sample)
}

```
#####Pull in the existing values, group into clean categories and output results to tsv.
```

#Load the yelp dataset
ColBusPrices <- read.csv("ColumbiaDataJoin.csv", header = TRUE, sep = ",", quote = "\"")

#combine using sqldf into a clean set with clean categories
sqlStr <- "Select PriceRange, Stars, 'Italian' as catagory, Name, url from ColBusPrices where categories like('%Italian%') AND Stars > 0 and PriceRange > 0  UNION ALL
           Select PriceRange, Stars, 'French' as catagory, Name, url from ColBusPrices where categories like('%French%') AND Stars > 0 and PriceRange > 0  UNION ALL
           Select PriceRange, Stars, 'American' as catagory, Name, url from ColBusPrices where categories like('%American%') AND Stars > 0 and PriceRange > 0 UNION ALL
           Select PriceRange, Stars, 'Indian' as catagory, Name, url from ColBusPrices where categories like('%Indian%') AND Stars > 0 and PriceRange > 0  UNION ALL
           Select PriceRange, Stars, 'Chinese' as catagory, Name, url from ColBusPrices where categories like('%Chinese%') AND Stars > 0 and PriceRange > 0  UNION ALL
           Select PriceRange, Stars, 'Japanese' as catagory, Name, url from ColBusPrices where categories like('%Japanese%') AND Stars > 0 and PriceRange > 0 "

#return clean dataset and convert factor colums to name
sample <- sqldf(sqlStr)
sample$Name = as.character(sample$Name)
sample$url = as.character(sample$url)
sample <- jitterSamples(sample)

#export to table for D3
write.table(sample, file = "C:/Users/Sam/Documents/HomeSVN/Python/EDAV/EDAV/yelpR/yelpR/output.tsv", append = FALSE, quote = FALSE, sep = "\t",
            eol = "\n", na = "NA", dec = ".", row.names = FALSE,
            col.names = TRUE, qmethod = c("escape", "double"),
            fileEncoding = "")

```
