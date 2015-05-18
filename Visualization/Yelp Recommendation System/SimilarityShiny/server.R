library(ggplot2)
library(ggmap)
library(dplyr)
library(leaflet)
library(shinyapps)
library(BH)

# Read in and format/manipulate data
business <- read.csv('yelpacademic_colleges/business_json.csv', header=T)
MF <- read.csv('MF_output_colleges.csv', header=T)
MF <- subset(MF, select = -c(X))
colnames(MF)[11] <- 'Link'
prices <- read.csv('restaurantprice.csv', header=T)
prices$X <- NULL
colnames(prices) <- c('business_id', 'price')
MF$id  <- 1:nrow(MF)
MF <- merge(MF, prices, by.x='business2', by.y='business_id', all.x=TRUE)
photo_url <- subset(business, select = c(business_id,photo_url))
MF <- merge(MF, photo_url, by.x='business2', by.y='business_id', all.x=TRUE)
MF <- MF[order(MF$id),] 
rownames(MF) <- MF$id
MF$id <- NULL
MF <- MF[,c(2, 1, 3,4,5,6,7,8,9,10,11,12,13)]
#MF$rank = as.factor(MF$rank)
#Jaccard <- read.csv('Jaccard_output.csv', header=T)
#Jaccard <- subset(Jaccard, select = -c(X))
#colnames(Jaccard)[10] <- 'Price'
#Jaccard$rank = as.factor(Jaccard$rank)

# Read in D3 files
file1 <- read.csv('www/vizdata.csv', header=T)

MF$name_base <- ''
for (i in 1:nrow(MF)) {
  if (((i-1)%%30) == 0) {
    temp = paste(as.character(MF$name[i]), as.character(MF$business1[i]))
  }
  MF$name_base[i] = temp
}

MF <- MF[order(MF$name_base, MF$rank),] 
rownames(MF) <- seq(1,nrow(MF))


# Get unique restaurant names
s <- seq(1, nrow(MF), 30)
main_rest <- MF[s,]
main_names_temp <- as.character(main_rest$name)
main_names <- c('All restaurants', main_names_temp)


for (i in 0:length(main_names)-1) {
  temp <- paste0(i, '. ', collapse='')
  main_names[i+1] <- paste0(temp, main_names[i+1])
}

# Run Shiny

library(shiny)

shinyServer = function(input, output, session) {
  react_output <- reactive ({
    # Get input from UI and split the string
    main_index <- strsplit(as.character(input$restname), '.',1)[[1]][1]
    main_index <- as.numeric(main_index)
    #main_index <- as.numeric(input$restname)
    if (!is.na(main_index)) {
      if (main_index != 0) {
        # If restaurant selected and not all restaurants
        # Get restaurant and top 10 similar restaurants from data frame
        restaurant <- 30*main_index
        rest1 <- MF[restaurant,1]
        similar <- MF[MF$business1 == rest1,]   
        similar <- similar[1:11,]
        
        lat1 <- similar$latitude
        lon1 <- similar$longitude
        lat2 <- similar$latitude_similar
        lon2 <- similar$longitude_similar
        rank <- similar$rank
        name <- similar$name
        link <- similar$Link
        stars <- similar$stars
        price <- similar$price
        rank <- similar$rank
        photo <- as.character(similar[1,]$photo_url)
        loc <- data.frame(rank, name, stars, price, link, lat1,lon1,lat2,lon2)
      }
      else {
        # If all restaurants selected
        similar <- MF[s,]
        lat1 <- similar$latitude
        lon1 <- similar$longitude
        name <- similar$name
        link <- similar$Link
        stars <- similar$stars
        price <- similar$price
        rank <- similar$rank
        photo <- ''
        loc <- data.frame(name, stars, price, link, lat1,lon1)
      }
      
      # Get Yelp logo for central restaurant
      logo <- 'http://www.chem-dry.net/andersons.az/about/yelp-logo-icon.png'
      
      
      library(leaflet)
      
      # Format attributes into html
      name1 <- loc$name
      name <- paste('<b>Name:</b> ', loc$name)
      
      price1 <- loc$price
      price <- paste('<br><b>Price:</b> ', loc$price)
      
      rank1 <- loc$rank-1
      rank <- paste('<br><b>Similarity rank:</b> ', loc$rank-1)
      
      #p <- function(k) paste(rep_len('$',k), collapse='')
      #loc[,'price'][is.na(loc[,'price'])] <- 0
      #price1 <- mapply(p, loc[,'price'])
      #price <- paste('<br><b>Price:</b> ', price1)
      
      l <- function(k){
        temp <- paste('<a href=\"', k, collapse='')
        temp <- paste(temp, '">Link</a>', collapse='')
        return(temp)
      }
      link1 <- mapply(l, loc[,'link'])
      link <- paste('<br><b>Like:</b> ', link1)
      
      "<a href=\"http://www.google.com\">http://www.google.com</a>"
      #link1 <- loc$link
      #link <- paste('<br><b>Link:</b> ', loc$link)
      
      stars1 <- loc$stars
      stars <- paste('<br><b>Stars:</b> ', loc$stars)
      
      att <- paste(name, stars)
      att <- paste(att, price)
      if (main_index != 0) {
        att <- paste(att, rank)
      }
      loc$att <- paste(att, link)
      
      JSlink <-"L.icon({iconUrl: '"
      JSlink <- paste(JSlink, logo)
      JSlink <- paste(JSlink, "' ,iconSize: [30, 30]})")
      
      # Construct leaflet map and data table with restaurants
      if (main_index != 0) {
        m = leaflet() %>% addTiles() %>% 
          addMarkers(loc$lon1[1], loc$lat1[1], icon = JS(JSlink), popup=loc$att[1]) %>%
          addCircleMarkers(data = loc, lat = lat2, lng = lon2, popup=loc$att, color = c('red',rep_len('green',10)), radius= ~ 15-rank, fillOpacity = 0.5) 
        data_shiny <- data.frame(name1, stars1, price1, rank1, link1)
        colnames(data_shiny) <- c('Restaurant', 'Stars', 'Price', 'Similarity', 'Link')
        newList=list("map"=m,"data"=data_shiny,"photo"=photo)
        return(newList)
      }
      else {
        m = leaflet() %>% addTiles() %>% 
          addCircleMarkers(data = loc, lat = lat1, lng = lon1, popup=loc$att, color = c(rep_len('green',length(main_names)-1)), radius = 3, fillOpacity = 0.5) 
        data_shiny <- data.frame(rep_len('',11),rep_len('',11),rep_len('',11),rep_len('',11),rep_len('',11))
        colnames(data_shiny) <- c('Restaurant', 'Stars', 'Price', 'Similarity', 'Link')
        newList=list("map"=m,"data"=data_shiny,"photo"=photo)
        return(newList)  
      }
    }})
  
  # Output map, restaurant information, and table of similar restaurants
  output$YelpMap = renderLeaflet(react_output()$map)
  output$table1 <- renderUI({
    data1 <- react_output()$data[1,]
    photo <- react_output()$photo
    photo <- paste0('<img src="',photo)
    photo <- paste0(photo,'" />')
    name <- paste0('<b>Restaurant: </b>', as.character(data1$Restaurant))
    stars <- paste0('<b>Stars: </b>', as.character(data1$Stars))
    price <- paste0('<b>Price: </b>', as.character(data1$Price))
    link <- as.character(data1$Link)
    output <- HTML(c(photo, '<br>', name,'<br>',stars,'<br>',price,'<br>',link))
    output
  })
  #renderDataTable({
  #data1 <- react_output()$data[1,]
  #data1
  #}, options = list(pageLength = -1, searching = FALSE), escape = FALSE)
  output$table2 <- renderDataTable({
    data2 <- react_output()$data[2:11,]
    data2
  }, options = list(pageLength = -1, searching = FALSE), escape = FALSE)
  # An observer is used to send messages to the client. 
  # The message is converted to JSON 
  observe({ session$sendCustomMessage(type = 'FoodMap', message = list(restname = input$restname)) })
}