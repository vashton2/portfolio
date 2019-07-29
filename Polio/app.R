library(shiny)
library(shinydashboard)
library(tidyverse)
library(plotly)
library(readr)
library(rworldmap)
library(classInt)
library(RColorBrewer)
library(digest)
library(leaflet)
library(shinyWidgets)
library(countrycode)
#library(pander)
library(stringr)

###### READING in STUFF

polio.vax <- read_csv("https://github.com/vashton2/portfolio/raw/master/data/polio-vaccine-coverage-of-one-year-olds.csv")

dat.polio <- read_csv("https://github.com/vashton2/portfolio/raw/master/data/progress-towards-polio-eradication.csv")

polio.occur <- read_csv("https://github.com/vashton2/portfolio/raw/master/data/the-number-of-reported-paralytic-polio-cases.csv")


###### Wrangling!!!


polio.all <- inner_join(polio.vax, polio.occur, by = c("Entity", "Year"), copy = FALSE)

polio.all <- inner_join(polio.all, dat.polio, by = c("Entity", "Year"), copy = FALSE) 

polio.all <- polio.all %>% 
    mutate(ImmunCoverPer = `Polio (Pol3) immunization coverage among 1-year-olds (WHO 2017) (%)`) %>% 
    mutate(Status = `Polio status (GPEI (2017))`) %>% 
    mutate(Cases = `Number of polio cases (WHO (2017))`) %>% 
    select(Entity, Year, Code, ImmunCoverPer, Status, Cases)

Entity.polio <- polio.all %>% 
    group_by(Entity) %>% 
    summarise(n = n()) %>% 
    select(Entity)

pal <- colorNumeric("viridis", NULL)

#### Define UI for application that draws a histogram
ui <- dashboardPage(
    dashboardHeader(title = "Polio Project"),
    dashboardSidebar(
        sidebarMenu(
            menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
            menuItem("Map", tabName = "Map", icon = icon("th")),
            menuItem("Thoughts", tabName = "model", icon = icon("th")))),
    
    dashboardBody(
        tabItems(
            
            ############################################################################################################
            ### Page One stuff ###
            
            
            tabItem(tabName = "dashboard",
                    
                    fluidRow(
                        box(plotlyOutput("plot1", height = 600), width = 9),
                        
                        box(
                            title = "Controls",
                            width = 3,
                            selectInput("Graphs", "Select a Graph: ", choices = c("Occurrences vs Year (Graph 1)", "Status vs Year (Graph 2)", "Interactive Graph", "Differences (Graph 3)"), selected = NULL),
                            pickerInput("checkGroup", "Select For the Interactive Graph",Entity.polio$Entity , selected = NULL, multiple = TRUE))),
                    
                    fluidRow(
                        tabBox(
                            title = "",
                            id = "tabset,", width = 12,
                            tabPanel("Graph 1", textOutput("Words1")),
                            tabPanel("Graph 2", textOutput("Words2")),
                            tabPanel("Graph 3", textOutput("Words3"))))),
            
            ############################################################################################################
            ### Page Two ###
            
            tabItem(tabName = "Map",
                    leafletOutput("map"), 
                    fluidRow(
                        box(title = "Controls",
                            sliderInput("range", "Year", min(polio.all$Year), max(polio.all$Year), value = 1, step = 1), 
                            selectInput("MapSelect", "Select :", choices = c("Immunization", "Occurrences"), selected = NULL))), 
                    fluidRow(box(textOutput("Words4")))),
            
            
            ############################################################################################################
            ### Third Tab Content ###
            
            tabItem(tabName = "model",
                    fluidRow(box(textOutput("Words"), width = 9)),
                    fluidRow(box(textOutput("Wordz"), width = 9)),
                    fluidRow(box(textOutput("Wordz2"), width = 9)),
                    fluidRow(box(textOutput("Wordz3"), width = 9)))
        )))




# Define server logic required to draw a histogram
server <- function(input, output) {
    
    
    ### tab outout
    
    output$tabset <- renderText({
        input$tabset1
    })
    
    
    output$plot1 <- renderPlotly({
        ############################################################################################################
        ### Interactive ###
        
        ConvsYear <- polio.all %>% 
            filter(Entity %in% c(input$checkGroup)) %>% 
            ggplot(aes(x = Year, y = Cases, color = Entity)) +
            geom_point() +
            geom_line(aes(group = Entity, color = Entity)) +
            theme_light() +
            theme(legend.position = "none") +
            labs(y = "Reported Occurrences", title = "The Decrease of Polio Occurrences")
        
        ############################################################################################################
        ### Change this one ###
        
        df <- polio.all
        
        dat <- polio.all %>% 
            na.omit() %>% 
            filter(Cases != 0)
        
        MeanCases1 <- dat %>% 
            group_by(Year) %>% 
            summarise(MeanCases2 = mean(Cases))
        
        medCases <- dat %>% 
            group_by(Year) %>% 
            summarise(medCase = median(Cases))
        
        df <- inner_join(df, MeanCases1, by = "Year")
        df <- inner_join(df, medCases, by = "Year")
        
        df <- df %>% 
            mutate(country = Entity)
        
        data.frame(df)
        
        df$continent <- countrycode(sourcevar = as.data.frame(df)[, "country"],
                                    origin = "country.name",
                                    destination = "continent")
        df <- df %>% 
            as_tibble()
        
        df <- df %>% 
            mutate(diff = df$Cases - df$MeanCases2)
        
        df <- df %>% 
            mutate(medDiff = df$Cases - df$medCase)
        
        df1 <- df[with(df, order(-ImmunCoverPer, Entity)), ]
        
        DIff <- df1 %>%
            na.omit() %>% 
            ggplot(aes(x = Year, y = medDiff, fill = ImmunCoverPer , order = ImmunCoverPer)) +
            geom_bar(stat = "identity") +
            theme_bw() +
            theme(legend.position = c(0.8, 0.2), legend.text = element_text(size = 10, face = "bold")) +
            facet_wrap(~continent, scale = "free_y") +
            geom_hline(yintercept = 0, color = "red", size = 1) +
            labs(y = "", title = "", legend = "Immunization %")
        
        
        ############################################################################################################
        ### This one is OK ###
        
        OccvsYear <- polio.all %>% 
            ggplot(aes(x = Year, y = Cases/1000, color = Entity)) +
            geom_point() +
            geom_line(aes(group = Entity, color = Entity)) +
            theme_light() +
            theme(legend.position = "none") +
            labs(y = "Reported Occurrences (in 1,000)", title = "The Decrease of Polio Occurrences")
        
        ############################################################################################################
        ### Bar Chart ###
        
        StatvsYear <- polio.all %>% 
            group_by(Status, Year) %>% 
            summarise(n = n()) %>% 
            ggplot(aes(x = Status, y = n, fill = Status)) +
            geom_col() +
            theme_bw() +
            theme(legend.position = "none", axis.text.x = element_blank()) +
            facet_wrap(~Year) +
            labs(title = "The Shift From Endemic to Certified Polio-Free")
        
        ############################################################################################################        
        
        data <- switch(input$Graphs, 
                       "Occurrences vs Year (Graph 1)" = OccvsYear, "Status vs Year (Graph 2)" = StatvsYear, "Interactive Graph" = ConvsYear,"Differences (Graph 3)" = DIff)
        
        ggplotly(data, tooltip = "all")
        
    })
    
    ############################################################################################################
    ### Maps ###
    
    output$map <- renderLeaflet({
        
        range <- polio.all %>% 
            filter(Year == as.numeric(input$range))
        
        sPDF <- joinCountryData2Map( range
                                     ,joinCode = "ISO3"
                                     ,nameJoinColumn = "Code")
        
        ImmunMap <- leaflet(sPDF) %>%
            addTiles() %>%
            addPolygons(stroke = FALSE, 
                        smoothFactor = 0.3, 
                        fillOpacity = 1,
                        fillColor = ~pal(ImmunCoverPer), 
                        label = ~paste0(Entity, ": ", ImmunCoverPer)) %>% 
            addLegend(pal = pal, values = ~ImmunCoverPer, opacity = 1.0, position = "bottomright")
        
        CasesMap <- leaflet(sPDF) %>%
            addTiles() %>%
            addPolygons(stroke = FALSE, 
                        smoothFactor = 0.3, 
                        fillOpacity = 1,
                        fillColor = ~pal(Cases), 
                        label = ~paste0(Entity, ": ", Cases)) %>% 
            addLegend(pal = pal, values = ~Cases, opacity = 1.0, position = "bottomright")
        
        outMap <- switch(input$MapSelect,
                         "Occurrences" = CasesMap, "Immunization" = ImmunMap)
        
        outMap
    })
    
    ############################################################################################################
    ### Words ###
    
    ### Words For tab 1 on page one
    output$Words1 <- renderText({
        paste("“Poliomyelitis (polio) is a highly infectious viral disease, which mainly affects young children. The virus is transmitted by person-to-person spread mainly through the faecal-oral route or, less frequently, by a common vehicle (e.g. contaminated water or food) and multiplies in the intestine, from where it can invade the nervous system and can cause paralysis. … There is no cure for polio, it can only be prevented by immunization.” (World Health Organization)", "
              In the 1950s vaccines were developed, and was primarily administered to the richer countries. In 1988 the Global Polio Eradication Initiative was founded and endeavored to rid the world of polio with their global vaccination campaign. When looking at graph one we see that India is affected the most by the disease but we see that there is a dramatic decrease from 1987 to 1991. It’s difficult to see each of the individual countries if you select the interactive graph in the controls back you can choose specifically which countries you want to look at. For the most part there was a general decrease from the 1980 and forward.", sep = "\n")
    })
    
    ### Words for tab 2 page one
    output$Words2 <- renderText({
        paste("Our second graphic depicts the progression of counties moving from the ‘danger’ or ‘epidemic’ status. At the beginning of the 1980s over half of the recorded countries were holding the status ‘epidemic’. This gives us a clearer picture of how on a world scale the major years of change happened from 1994 to 2001, we go from over 50 countries in the ‘epidemic’ status to nearly all of them are ‘polio-free’ status. Suggesting that at least time caused the decline of polio. ")
    })
    
    ### Words for tab 3 page one
    output$Words3 <- renderText({
        paste("Our final graph shows the difference between the observed amount of polio cases and the median amount of reported polio cases. The bar above the red line would be all the recorded occurrences that are more than the median while bars below the red line are the observations that were below the median count. I’m using the median to prevent outlier countries from causing a huge skew in our graph. When looking at these graphs we see that most of the lower immunization coverage for the population corresponded with a higher amount of polio occurrences. This is particularly prevalent in the Asia graph until about 2000, where it equalized. Something that might be misleading with this graph is that low bars on either side of the equation, this indicates that the number of occurrences is about the same as the median. Once we understand the graph correctly it does show that the higher the immunization percentage in a population the more often that population is under the median amount.")
    })
    
    ### Words for map
    output$Words4 <- renderText({
        paste("This map allows you to see the percent of the population that has been immunized for each of the individual countries for any given year, use the slider to go between years, or change it to “Occurrences”, to see the amount of occurrences in a given country based off of the year.")
    })
    
    
    ### Words For Thoughts page 
    
    output$Words <- renderText({
        paste("Something that was annoying with this data was that it was comprised of summaries, or at least it felt that was, it didn’t have individual dates and places just the total for the year and country. I had to link the immunization percentage, the epidemic status, and the recorded cases together, it wasn’t too hard.  Creating a shiny dashboard only allowed a little bit of generic wrangling you had to be careful of where you changed things otherwise it would mess up all of the other graphs. I recognize that each of my graphs at the core of it all shows the same thing and it would be better to use different graphics to deepen understanding.") })
    
    
    output$Wordz <- renderText({
        paste("For my map I would have liked to get actually latitude and longitude points for each of the countries but I didn’t get around to finding that so I used rworldmap package, this doesn’t allow me to set a viewing window in leaflet, so it always starts zoomed out. Something else I would like to change would be the slide rule, I like how you can select your a specific year, but I want something smoother that would allow the view to see the progression a little bit easier.  Maybe as the map extends it shows shows that change year by year as you scroll along. Or at least a smooth transition from year to year.") })
    
    output$Wordz2 <- renderText({
        paste("Another thing that I would like to fix would be the differences graph, I think it’s something to do with  ggplotly but the Americas and the Oceana graphs are a little more squished than the other graphs and they shouldn’t be. Also my theme() function to fix the legend isn’t working and I haven’t figured out why, hence the badly labeled and positioned legend. I know stack bar charts aren’t always the best option but I think you can find some good insight to this graph, will keep until a better one comes along.") })
    
    output$Wordz3 <- renderText({
        paste("In the future I would like to get some weather, something that has the major natural disasters, and their locations to see if there is any correlation there, and I would like to keep searching for reliable data that goes back further than 1980. I would also like to compare the rise and fall of other viral diseases to confirm that they follow the same pattern when vaccines are created. It would also be interesting to find the most common words that are associated with vaccines from the media, to see if there still needs to be a different train of thought started on the topic.
")
    })
    
    
    
}

shinyApp(ui, server)