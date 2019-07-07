library(dplyr)
library(shiny)
library(shinydashboard)

## Load data into memory
beer_info <- data.table::fread(input="../data/beer_info.csv")
beer_ratings <- data.table::fread(input="../data/beer_ratings.csv")
print(beer_info %>% head)
