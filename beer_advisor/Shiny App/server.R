library(shiny)
library(DT)

shinyServer(function(session,input, output) {
  addClass(selector = "body", class = "sidebar-collapse")
  
  vars = reactiveValues()
  
  vars$Beer <- "Yakima Fresh Hop"
  
  ##################################################################
                     ##Selector Values Update##
  ##################################################################
  vars$Family <- "India Pale Ales"
  vars$Style <- "American IPA"
  
  observeEvent(input$SelectFamily,{
    vars$Family <- input$SelectFamily
    styles = beer_family %>% filter(family == vars$Family) %>% select(style)
    updateSelectInput(session,input="SelectStyle", choices=styles)
  })
  observeEvent(input$SelectStyle,{
    vars$Style <- input$SelectStyle
    
    beers = beer_info %>% 
      select(beer_style,brewery,BAscore,beer_name) %>%  filter(beer_style == vars$Style) %>% 
      select(-beer_style) %>%   group_by(brewery)
    updateSelectInput(session,input="SelectBeer", choices=beers$beer_name)
  })
  
  
  ##################################################################
                      ##Beer Selection Update##
  ##################################################################
  vars$Beer <- "Yakima Fresh Hop"
  vars$beer_id <- 1
  vars$img_src <-"https://cdn.beeradvocate.com/im/beers/141544.jpg"
  
  
  observeEvent(input$SelectBeer, {
    vars$Beer <- input$SelectBeer
    vars$beer_id <- beer_info %>% filter(beer_name == vars$Beer) %>% select(beer_id) %>% .[1,1]
    vars$img_src <- beer_info %>% filter(beer_name == vars$Beer) %>% select(beer_img) %>% .[1,1]
    output$picture<-renderText({c('<img src="',vars$img_src,'">')})
  })
  
  observeEvent(input$SearchBeer, {
    vars$Beer <- input$SearchBeer
    vars$beer_id <- beer_info %>% filter(beer_name == vars$Beer) %>% select(beer_id) %>% .[1,1]
    vars$img_src <- beer_info %>% filter(beer_name == vars$Beer) %>% select(beer_img) %>% .[1,1]
    output$picture<-renderText({c('<img src="',vars$img_src,'">')})
  })
  
 
  
  output$InfoBoxName <- renderText({paste('Name:', vars$Beer)})
  output$InfoBoxBrewery <- renderText({paste('Brewery: ', beer_info %>% filter(beer_id == vars$beer_id) %>% select(brewery) %>% .[1,1])})
  output$InfoBoxScore <- renderText({paste('Score: ',beer_info %>% filter(beer_id == vars$beer_id) %>% select(BAscore) %>% .[1,1])})
  output$InfoBoxABV <- renderText({paste('ABV: ',beer_info %>% filter(beer_id == vars$beer_id) %>% select(abv) %>% .[1,1])})
  output$InfoBoxRanking <- renderText({paste('Ranking: ',beer_info %>% filter(beer_id == vars$beer_id) %>% select(ranking) %>% .[1,1])})
  output$InfoBoxDesc <- renderText({beer_info %>% filter(beer_id == vars$beer_id) %>% select(desc) %>% .[1,1]})
  
 # output$Desc <- renderText({beer_info %>% filter(beer_id == var$beer_id) %>% select(desc) %>% .[1,1]})
  
  
  ##################################################################
                   ##Add Beer Update##
  ##################################################################
  vars$user_list <- data.frame(names = c(), id = c(),scores = c()) 
  observeEvent(input$AddBeer, {
    
    
    vars$user_list <- rbind(vars$user_list, data.frame(names = vars$Beer, id = vars$beer_id, scores = input$user_score))
    vars$user_list = vars$user_list[!duplicated(vars$user_list[,c("id")],fromLast=T),]
    
    output$BeerList <- DT::renderDataTable(
      vars$user_list %>% rename(Beer = names, Score = scores) %>% select(Beer, Score),
      
    )
    
  })
  
  observeEvent(input$GenRecs, {
    ids = as.numeric(unlist(vars$user_list %>% select(id) %>% list))
    scores = as.numeric(unlist(vars$user_list %>% select(scores) %>% list))
    print(typeof(ids))
    print(typeof(scores))
    recs = generate_recommendations(ids,scores,beer_info,beer_ratings)
    print(recs)
    output$BeerRecs <- DT::renderDataTable(
      recs %>% rename(Beer = beer_name, Score = BAscore,Brewery=brewery,Style=beer_style)
      
    )
    
  })
  
  
  
  
  
  
  
  
})
