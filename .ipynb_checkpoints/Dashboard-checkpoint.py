################################################ New York Citibikes Dashboard #################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initializing settings for the dashboard ##################################################################

st.set_page_config(page_title = 'New York Citibikes Strategy Dashboard', layout='wide')
st.title("New York Citibikes Strategy Dashboard")
st.markdown("The dashboard will help with the distribution problems New York Citibike currently faces.")
st.markdown("Citibike, New York's bike-sharing service, has been increasing in popularity since its inception in 2013. Demand for bikes has especially risen after the Covid-19 pandemic and has led to distribution issues. Customers are finding some stations to be sparse, preventing them from renting bikes, and other stations to be full, preventing them from returning bikes. This analysis aims to determine where and why issues arise.") 

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top_20_stations = pd.read_csv('top_20_stations.csv', index_col = 0)

########################################## DEFINE THE CHARTS #####################################################################

##bar chart
fig = go.Figure(go.Bar(x = top_20_stations['start_station_name'], y = top_20_stations['value'], marker={'color': top_20_stations['value'],'colorscale': 'Greens'}))
fig.show()

fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)

st.plotly_chart(fig, use_container_width=True)

##line chart

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['daily_bike_rides'], name = 'Daily bike rides', marker={'color': df['daily_bike_rides'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily Bike Trips and Temperatures in New York City 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)

### Adding the map ###

path_to_html = "New_York_Citibike_Trips.html" 

# Read file and keep in variable
with open(path_to_html,'r', errors='replace') as f: 
    html_data = f.read()

## Show in webpage
st.header("Top 100 Most Popular Bike Trips in New York City")
st.components.v1.html(html_data,height=1000)