library(shiny)

shinyUI(
    dashboardPage(
        dashboardHeader(title="Beer Advisor"),
        dashboardSidebar(
            sidebarMenu(
                menuItem("Enthusiasts",tabName = "Recommender",icon=icon("globe")),
                menuItem("Brewers", tabName = "For Brewers", icon=icon("database"))
            )
        )
    ),
    dashboardBody(
        tabItems(
            tabName="Recommender",
            fluidRow(column(width=4,
                            selectInput("")))
        )
    )
)