library(shiny)
library(leaflet)

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

# Scaling variables: xFrame=300,yFrame=300,width=300,height=300,scaleFactor=110

fileName <- 'index.html' 
FoodMap <- readChar(fileName, file.info(fileName)$size)
#FoodMap <- 'test'

# Run Shiny UI - specifying title, leaflet map, restaurant information, and similar restaurant table
shinyUI = fluidPage(fluidRow(column(2,img(src='header_logo.png', width=150, height=75)),
                             column(10,titlePanel('Recommendation System'), style = "color: white"),
                             style = "background-image: url('background-red.jpg')",
  mainPanel('Once you choose a restaurant, bubble sizes indicate similarity', style = "color: white")),
  fluidRow(column(8,leafletOutput('YelpMap',width = "100%", height = 600)),
                column(4,wellPanel(span(htmlOutput("table1"))),
                       wellPanel('Most popular food items:', HTML(FoodMap), includeCSS("foodMap.css")))),
       fluidRow(
         wellPanel(
           selectizeInput('restname', "Pick a Restaurant:", choices=main_names, multiple = FALSE, options = list(placeholder = 'Type in restaurant name')),
           singleton( tags$head(tags$script(src = "d3.v3.min.js"))),
           singleton( tags$head(tags$script(src = "d3.tip.min.js"))),
           singleton( tags$head(tags$script(src = "foodMap.js"))))),
       fluidRow(dataTableOutput(outputId="table2")),
       fluidRow(HTML('<a href="http://run.plnkr.co/plunks/jRIGKXMZLDn5xrMJgqTl/">Switch to Yelp User Preference Search</a>')))
