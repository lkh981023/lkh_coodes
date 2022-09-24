library(shiny)
library(stringr)
library(tidyverse)
library(fuzzyjoin)
library(leaflet)
library(lubridate)
library(ggplot2)
library(shinythemes)
wd <- getwd() ## get working directory
setwd(wd) # set working directory
flight_data = read_csv('RFDS_flightdata_July2022_PE2.csv') # read data
base_data = read_csv('RFDS_bases_PE2.csv') 

###Map
join_data = flight_data %>%
  fuzzy_inner_join(base_data, by = c('Destination' = 'Location'),
                   match_fun = str_detect) ## using fuzzy join to match the partly same
#string, this code is design from the reference below.
#####reference:https://stackoverflow.com/questions/61000838/fuzzy-left-join-with-r

join_data$ArrivedHour = NA #create a new column
join_data$ArrivedHour = hour(join_data$ArrivalAEST)#transfer the time data into hour
join_data$ArrivedMin = NA
join_data$ArrivedMin = minute(join_data$ArrivalAEST)

  


join_data %>%group_by(Location) %>% 
  mutate(Arrival_count = n()) %>% 
  filter(ArrivedHour > 1 & ArrivedHour < 17) %>%
  group_by(Location, Longitude, Latitude,Arrival_count) %>%
  count(name = 'Total_num') %>%
  leaflet() %>%
  addTiles() %>%
  addCircleMarkers(lng = ~Longitude,
                   lat = ~Latitude,
                   radius = ~Total_num,
                   popup = ~paste('Flight Base Name: ', Location, 'Selcted time range flight count: ',
                                  Total_num,'Total Arrival aircraft: ',
                                  Arrival_count)) %>%
  addProviderTiles(providers$Esri.NatGeoWorldMap) ## draw a map.design from the reference below
##reference:https://rstudio.github.io/leaflet/morefeatures.html

#######Select QLD base for visualization

QLD_base = c('Cairns','Townsville',
             'Rockhampton','Bundaberg',
             'Brisbane','Charleville','Roma',
             'Longreach','Mount Isa')# select the location name belongs to QLD

####Visual 1

Visual_1 = join_data %>%
  filter(Location %in% QLD_base) %>%
  mutate(numeric_Time = as.numeric(ArrivedHour,'.',ArrivedMin)) %>% ##transfer the data from factor to numeric type
  mutate(Arrival_DayNight = if_else(numeric_Time > 6.00 & numeric_Time < 18.00, 'Day','Night'))%>% 
  ggplot(aes(x = Location, fill = Arrival_DayNight)) +
  geom_bar() +
  scale_fill_manual(
    values = c(Day = "#FBC244",
               Night = "#0186D2")
  ) +
  labs(
    x = "Location",
    y = "Number",
    title = "Number of flight arrived at QLD bases"
  ) +theme(axis.text.x = element_text(angle = 45, size = 8)) ##set the format of x-axis
   # Draw visulaization 1


# ###Visual 2

Visual_2_data = join_data %>%
  filter(Location %in% QLD_base) %>% ## filter out the QLD bases info from data
  group_by(Location) %>% count(name = 'Total_num') %>%
  arrange(desc(Total_num)) %>%
  head(4) ## select first four location that has been most visited.

Visual_2 = join_data %>% mutate(numeric_Time = as.numeric(ArrivedHour,'.',ArrivedMin)) %>% 
  mutate(Arrival_DayNight = if_else(numeric_Time > 6.00 & numeric_Time < 18.00, 'Day','Night')) %>%
  filter(Location %in% Visual_2_data$Location) %>%
  group_by(Location, Arrival_DayNight,ArrivedHour) %>%
  count(name = 'Count_num') %>% 
  ggplot(aes(x = ArrivedHour, y = Count_num, fill = Arrival_DayNight)) +
  geom_col(width = 0.8) +scale_fill_manual(values = c(Day = "#EB990B",
                                                      Night = "#0D4FE0"))+
  labs(title = 'TOP4 Queensland RFDS
bases visited')+ theme_bw()+
  facet_wrap(~Location) ## draw visualization 2
## generate four different graph based on the location


# ###Shiny
ui = fixedPage(shinythemes::shinytheme('yeti'),
  fixedRow(
    titlePanel('QUEENSLAND AIR BASES USED BY THE RFDS, JULY 2022')

  ),
  fixedRow(
    substitute('This visualization project is mainly illustrate the RFD aircraft
    data in July, 2022. Specifically, the dataset that used in visualization are record
    of RFDS flight in Australia in July 2022 and the bases that currently used by
    RFDS in Australia.
               ')
  ),
  fixedRow(
    column(5,
           tags$b('Location of bases'),
           tags$br(),'This map shows all bases that currently used by RFDS.
           Sepcifically, the radius of circle represent the total number of aircraft arrived at
           RFDS bases within selcted time range. The larger radius of circle means higher
           number of arrival aircraft under the selected time range.'),
    column(7,
           sliderInput('TimeRange',
                       'Arrival Time Range within 24 hours:',
                       min = 0,
                       max = 23,
                       value = range(join_data$ArrivedHour, na.rm = TRUE)

           ),
           leafletOutput('Map'))
  ),
  fixedRow(column(5,
                  plotOutput('Visual1')),
           column(2,
                  tags$b('Time of Travel'),
                  tags$br(),
                  'These two groahs shows the arrival informtion of RFDS aircrafts
                  in QLD bases. To be more specific, there are nine RFDS
                  bases located at QLD. The visualization at left corner of web page
                  (Visual1)shows the total number of aircraft arrived at QLD bases within
                  Day(6am-6pm),Night(6pm-6am) Range. The visualization at rght corner
                  of web page(Visual2) shows the number of times that flight arrived each
                  hour at the first four QLD RFDS bases visited, according to
                  Visual 2'),
           column(5,
                  plotOutput('Visual2')))
)


server = function(input,output){
  output$Map = renderLeaflet({join_data %>%group_by(Location) %>% 
      mutate(Arrival_count = n()) %>% 
      filter(between(ArrivedHour, input$TimeRange[1],input$TimeRange[2])) %>%
      group_by(Location, Longitude, Latitude, Arrival_count) %>%
      count(name = 'Total_num') %>%
      leaflet() %>%
      addTiles() %>%
      addCircleMarkers(lng = ~Longitude,
                       lat = ~Latitude,
                       radius = ~Total_num,
                       popup = ~paste('Flight Base Name: ', Location, 'Total flight number: ',
                                      Arrival_count, 'Selcted time range flight count: '
                                      ,Total_num))%>%
      addProviderTiles(providers$Esri.NatGeoWorldMap)

  })
  output$Visual1 = renderPlot({
    join_data %>%
      filter(Location %in% QLD_base) %>%
      mutate(numeric_Time = as.numeric(ArrivedHour,'.',ArrivedMin)) %>% 
      mutate(Arrival_DayNight = if_else(numeric_Time > 6.00 & numeric_Time < 18.00, 'Day','Night'))%>% 
      ggplot(aes(x = Location, fill = Arrival_DayNight)) +
      geom_bar() +
      scale_fill_manual(
        values = c(Day = "#FBC244",
                   Night = "#0186D2")
      ) +
      labs(
        x = "Location",
        y = "Number",
        title = "Number of flight arrived at QLD bases"
      ) +theme(axis.text.x = element_text(angle = 45, size = 8))
  })
  output$Visual2 = renderPlot({ 
    join_data %>% mutate(numeric_Time = as.numeric(ArrivedHour,'.',ArrivedMin)) %>% 
      mutate(Arrival_DayNight = if_else(numeric_Time > 6.00 & numeric_Time < 18.00, 'Day','Night')) %>%
      filter(Location %in% Visual_2_data$Location) %>%
      group_by(Location, Arrival_DayNight,ArrivedHour) %>%
      count(name = 'Count_num') %>% 
      ggplot(aes(x = ArrivedHour, y = Count_num, fill = Arrival_DayNight)) +
      geom_col(width = 0.8) +scale_fill_manual(values = c(Day = "#EB990B",
                                                          Night = "#0D4FE0"))+
      labs(title = 'TOP4 Queensland RFDS
bases visited')+ theme_bw()+
      facet_wrap(~Location)
  })
}

shinyApp(ui = ui, server = server)


