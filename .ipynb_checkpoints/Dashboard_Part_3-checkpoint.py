###########################################Importing Libraries##############################################
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initializing settings for the dashboard ########################################

st.set_page_config(page_title = 'New York Citibikes Strategy Dashboard', layout='wide')
st.title("New York Citibikes Strategy Dashboard")

# Defining side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro Page","Weather and Bike Usage",
   "Most Popular Stations",
    "Interactive Map with Most Popular Bike Trips", "Weather and Bike Type", "Recommendations"])

########################################Importing Data######################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top_20_stations = pd.read_csv('top_20_stations.csv', index_col = 0)

#####################################Defining the pages####################################################
###Creating intro page ###

if page == "Intro Page":
    st.markdown("This dashboard will help with the distribution problems New York Citibike currently faces.")
    st.markdown("Citibike, New York's bike-sharing service, has been increasing in popularity since its inception in 2013. Demand for bikes has especially risen after the Covid-19 pandemic and has led to distribution issues. Customers are finding some stations to be sparse, preventing them from renting bikes, and other stations to be full, preventing them from returning bikes. This analysis aims to determine where and why issues arise.  The dashboard is separated into 5 sections:") 
    st.markdown("- Weather and Bike Usage")
    st.markdown("- Most Popular Stations")
    st.markdown("- Interactive Map With Most Popular Trips")
    st.markdown("- Weather and Bike Type")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis.")

    myImage = Image.open("Citibikes.jpg") #source: https://unsplash.com/photos/a-row-of-blue-bicycles-parked-next-to-each-other-OGaaDTtttvI
    st.image(myImage)
    st.markdown("Source: https://unsplash.com/photos/a-row-of-blue-bicycles-parked-next-to-each-other-OGaaDTtttvI")

### Creating the dual axis line chart page ###

elif page == 'Weather and Bike Usage':
    
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
go.Scatter(x = df['date'], y = df['daily_bike_rides'], name = 'Daily Bike Rides', marker={'color': df['daily_bike_rides'],'color': 'blue'}),
secondary_y = False
)

    fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily Temperature', marker={'color': df['avgTemp'],'color': 'red'}),
secondary_y=True
)

    fig_2.update_layout(
    title = 'Daily Bike Trips and Temperatures in New York City 2022',
    height = 600,
)

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is a clear correlation between temperature and daily bike rides.  As temperature increases, so does the number of daily bike rides.  When temperature decreases, the number of daily bike rides decreases as well.  This suggests that shortage issues may occur primarily during the warmer months, namely April to November.")

###Creating Most Popular Stations Page###
  # Creating the season variable
elif page == 'Most Popular Stations':
    
# Creating the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
# Defining the total rides
    total_rides = float(df1['daily_bike_rides'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

# Calculating top 20 stations based on df1 because it contains seasons 
    top_20_stations = (
    df1.groupby('start_station_name')['daily_bike_rides']
    .count()
    .reset_index()
    .rename(columns={'daily_bike_rides': 'value'})
    .sort_values(by='value', ascending=False)
    .head(20)
)
##bar chart###
    fig = go.Figure(go.Bar(x = top_20_stations['start_station_name'], y = top_20_stations['value'], marker={'color': top_20_stations['value'],'colorscale': 'Greens'}))

    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From this bar chart, it is clear that some start stations are utilized more than others.  The top 3 stations are West St/Chambers St, W 21 St/6th Ave, and Broadway/W 58 St.  The number of rides originating from these stations is a steep increase from the number of rides originating from the rightmost stations on the chart.  This suggests a strong preference for the aforementioned stations.") 

elif page == 'Interactive Map with Most Popular Bike Trips': 

### Creating the map ###

    st.write("Interactive map showing most popular bike trips in New York City")

    path_to_html = "New_York_Citibike_Trips.html" 

### Read file and keep in variable ###
    with open(path_to_html,'r', encoding='utf-8') as f: 
        html_data = f.read()
### Show in webpage ###
    st.header("Top 100 Most Popular Bike Trips")
    st.components.v1.html(html_data,height=400)    
    st.markdown("##### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown(" - West St./Chamber St.")
    st.markdown(" - W 21st/6th Ave.")
    st.markdown(" - Broadway/W 58th St.")
    st.markdown("When using the trip filter, we can see that West St./Chambers St. and W 21st/6th Ave appear in some of the most common trips.  However, Broadway/W 58th St does not.")  
    st.markdown("The most common routes are between:")
    st.markdown("- 7th Ave/Central Park South.")
    st.markdown("- Central Park South/6th Ave.")
    st.markdown("- Roosevelt Island Tramway.")


elif page == 'Weather and Bike Type':
###Creating facegrid for bike types###    
###importing data set that has rideable_type 
    import plotly.express as px
    df2 = pd.read_csv('weather_and_daily_bike_rides_data_smallest_subset.csv', index_col = 0)
    fig = px.histogram(
    df2, 
    x="avgTemp", 
    facet_col ="rideable_type",  
    nbins=15,              
    title="Average Temperature Distribution by Bicycle Type",
    labels={"avgTemp": "Average Temperature", "rideable_type": "Bicycle Type"},
        color="rideable_type",  
        color_discrete_map={
        "electric_bike": "lightgreen", 
        "classic_bike": "darkgreen"
    })
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("This chart shows that overall classic bikes are used more frequently than electric bikes.  Both types of bikes are ridden more in warmer temperatures, with the frequency of bike rides peaking between 20-25 degrees, though the peak is much higher for classic bikes than it is for electric bikes.  For classic bikes, there is a steep increase at 10 degrees while for electric bikes the increase is more gradual. This indicates a strong preference for warmer temperatures in classic bike riders.  Electric bike rides are more evenly distributed across temperatures.")
        
else: 
   
    st.header("Conclusions and recommendations")
    bikes = Image.open("Citibikes_2.jpg")  #source: Unsplash
    st.image(bikes)
    st.markdown("Source: https://unsplash.com/photos/man-in-black-jacket-riding-blue-bicycle-on-street-during-daytime-DMt6OBEPmo8")
    st.markdown("#### Our analysis has shown that Citibikes should focus on the following objectives:")
    st.markdown("- Add more stations around Central Park South and at the Roosevelt Island Tramway as these are where the most common trips take place.")
    st.markdown("- Ensure that bikes are well stocked at the most popular stations during the warmer months but decrease the supply during the colder months.")
    st.markdown("- When adding more bikes for warmer temperatures, add primarily classic bikes as those are more popular.")
