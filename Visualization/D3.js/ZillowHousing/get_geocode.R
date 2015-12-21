data = read.csv('Metro_MedianRentalPrice_1Bedroom.csv', sep = ",")
data$RegionName <- as.character(data$RegionName)

library(ggmap)
#geocode(data[2,1])

data$latitude <- NA
data$longitude <- NA
  
for(i in 1:nrow(data)) {
  data$longitude[i] <- geocode(data$RegionName[i])[1]
  data$latitude[i] <- geocode(data$RegionName[i])[2]
}

data$latitude <- as.numeric(data$latitude)
data$longitude <- as.numeric(data$longitude)

write.csv(data, file = "Metro_MedianRentalPrice_1Bedroom_Location.csv")
