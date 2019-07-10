library(shiny)

shinyUI(
    dashboardPage(
        dashboardHeader(title='Beer Advisor'),
        dashboardSidebar(),
        dashboardBody(
            useShinyjs(),
            fluidRow(box(width=3,
                         column(width=12,selectInput("SelectFamily","Pick a Family of Beer Styles",choices = families)),
                         column(width=12,selectInput("SelectStyle","Pick a Beer Style",choices = "")),
                         column(width=12,selectInput("SelectBeer","Pick a Beer",choices = "")),
                         column(width=12,selectizeInput("SearchBeer", "Write in a Beer", beer_info %>% select(beer_name), selected = NULL, multiple = FALSE,options = NULL))),
                     box(width=9,
                         column(width=12,
                                box(width=4,
                                    htmlOutput("picture")
                                    
                                ),
                                box(width = 8,
                                    h3(textOutput('InfoBoxName')),
                                    h4(textOutput('InfoBoxBrewery')),
                                    column(width=4,
                                           h5(textOutput('InfoBoxABV')),
                                           h5(textOutput('InfoBoxRanking')),
                                           h5(textOutput('InfoBoxScore'))),
                                    column(width=8,
                                           textOutput('InfoBoxDesc'))
                                    ),
                                box(width=6,
                                    column(6,
                                           actionButton('AddBeer',"Add Beer to List", icon = NULL, width = NULL)),
                                    column(6,
                                           sliderInput("user_score","How much do you like it?",min=1,max=5,step=0.1,value=50)))
                                
                         )
                     )
            ),
            fluidRow(box(width=12,
                         box(width=6,
                             DT::dataTableOutput('BeerList')
                             ),
                         box(width=6,
                             actionButton('GenRecs',"Find Recommendations", icon = NULL, width = NULL),
                             DT::dataTableOutput('BeerRecs')
                             
                             )))
        )
    )
)






                
                



