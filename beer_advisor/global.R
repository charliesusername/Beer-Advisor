library(dplyr)
library(shiny)
library(shinydashboard)
library(reticulate)
source_python("scripts/top5beers.py")

## Load data into memory
beer_info <- data.table::fread(input="../data/beer_info.csv")
beer_ratings <- data.table::fread(input="../data/beer_ratings.csv")
beer_family <- data.table::fread(input='../data/beer_family_lookup.csv',
                                 header = TRUE) %>% select(family,style)

families = beer_family %>% select(family) %>% unique()

user_list <- data.frame(
  beers = c(),
  scores = c()
)



  
