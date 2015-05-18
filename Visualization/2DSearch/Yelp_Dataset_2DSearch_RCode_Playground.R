fileName <- 'yelp_academic_dataset_user.csv'
BarDBarBar <- readChar(fileName, file.info(fileName)$size)


#load csv's into memmory
user2 <- read.delim("yelp_academic_dataset_user.csv", dec=",")

ColUsers <- read.csv("Columbia_users_json.csv", header = TRUE, sep = ",", quote = "\"")

ColReviews <- read.csv("Columbia_reviews_json.csv", header = TRUE, sep = ",", quote = "\"")

ColBusiness <- read.csv("Columbia_business_json.csv", header = TRUE, sep = ",", quote = "\"")

ColBusPrices <- read.csv("ColumbiaDataJoin.csv", header = TRUE, sep = ",", quote = "\"")


#SQLlite read 
system("ls *.db", show=TRUE)
sqlite    <- dbDriver("SQLite")
exampledb <- dbConnect(sqlite,"C:/Users/Sam/Documents/HomeSVN/Python/EDAV/EDAV/yelpR/yelpR/test.sqlite")
dbListTables(exampledb)
results <- dbGetQuery(exampledb, "SELECT * FROM Users Where fans >50")
results <- dbGetQuery(exampledb, "SELECT * FROM Users ")

#SQLlite write
library(DBI)
library(RSQLite)
library(data.table)

driver = dbDriver("SQLite")
con = dbConnect(driver, dbname = "C:/Users/Sam/Documents/HomeSVN/Python/EDAV/EDAV/yelpR/yelpR/test.sqlite")
dbSendQuery(con, "DROP TABLE IF EXISTS user")
dbWriteTable(con, "ColReviews", ColReviews)
dbDisconnect(con)
dbUnloadDriver(driver)

############
Get Yelp API Info

# yelp
consumerKey = "9JybzZXBKxlzzW5geZIF1A"
consumerSecret = "j9LXGruAO0Xo_Rq9EJ5ec6-OtmM"
token = "LAqdY_HDUJgBBHELuOfd3smERbGlnB4C"
token_secret = "yUWS1nZCafLIWSwU4YIG-5KIAQI"


# authorization
myapp = oauth_app("YELP", key=consumerKey, secret=consumerSecret)
sig=sign_oauth1.0(myapp, token=token,token_secret=token_secret)

limit <- 10

# 10 bars in Chicago
yelpurl <- paste0("http://api.yelp.com/v2/search/?limit=",limit,"&location=Chicago%20IL&term=bar")
# or 10 bars by geo-coordinates
yelpurl <- paste0("http://api.yelp.com/v2/search/?limit=",limit,"&ll=37.788022,-122.399797&term=bar")

yelpurl <- "http://api.yelp.com/v2/business/uLnDFdn011hEroQQMLmxNQ"

locationdata=GET(yelpurl, sig)
locationdataContent = content(locationdata)
locationdataList=jsonlite::fromJSON(toJSON(locationdataContent))
head(data.frame(locationdataList))

#####################################


#function to jitter the samples
jitterSamples <- function(sample){
  for (i in 0: nrow(sample) - 1 ) 
  {
    sample[i,1] = sample[i,1] + runif(1, -.1, .1)
    sample[i,2] = sample[i,2] + runif(1, -.1, .1)
  }
  return(sample)
}

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



########################
#sqldf exploration of the data

sqlStr <- "Select count(business_id) from business where business_id in (Select business_id from review group by business_id) and categories like('%American%') "

sqlStr <- "Select user_id, count(*) as reviews from review group by user_id order by reviews desc LIMIT 100"
sqlStr <- "select review.stars, business.PriceRange, review.business_id, business.latitude, business.longitude, business.categories  from review JOIN business ON review.business_id = business.business_id  where  review.user_id = 'kGgAARL2UmvCcTRfiscjug'"

final <- sqldf(sqlStr)


sqlStr <- "Select avg(business.PriceRange) from business where categories like('%Chinese%') "
final <- sqldf(sqlStr)

test[1]


sqlStr <- "Select "


#############################

write.table(results3[0:800000,], file = "C:/Users/Sam/Documents/HomeSVN/Python/EDAV/EDAV/yelpR/yelpR/reviews1.csv", append = FALSE, quote = TRUE, sep = ",",
            eol = "\n", na = "NA", dec = ".", row.names = TRUE,
            col.names = TRUE, qmethod = c("escape", "double"),
            fileEncoding = "")


