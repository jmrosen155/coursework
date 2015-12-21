data = read.csv('data_wide.csv', sep = ",")
data$City <- as.character(data$City)

library(ggmap)
#geocode(data[2,1])

data$latitude <- NA
data$longitude <- NA
  
for(i in 1:nrow(data)) {
  data$longitude[i] <- geocode(data$City[i])[1]
  data$latitude[i] <- geocode(data$City[i])[2]
}

data$latitude <- as.numeric(data$latitude)
data$longitude <- as.numeric(data$longitude)

write.csv(data, file = "data_wide_location.csv")

