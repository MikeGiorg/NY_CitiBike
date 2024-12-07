############################################################## CITI BIKE DASHBOARD #############################################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

####################################################### Initial Setting for the Dashboard ######################################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout = 'wide')
st.title('Citi Bike Strategy Dashboard')
st.markdown('The dashboard will help with the expansion problems Citi Bike currently faces')
st.markdown('Right now, Citi Bike bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.')

################################################################## Import Data #################################################################################

bike = pd.read_csv(r'../Data/Prepared/dashdata.csv', index_col = 0)
top20 = pd.read_csv(r'../Data/Prepared/top20.csv', index_col = 0)

################################################################ Define the Charts #############################################################################

## Bar Chart ##

fig = go.Figure(go.Bar(x = top20['start_station'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'oranges'} ))
fig.update_layout(
    title = '20 Most Popular Bike Stations in NY', 
                  xaxis_title = 'Start Stations', 
                  yaxis_title = 'Trips', 
                  width = 900, 
                  height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line Chart ##

fig_2 = make_subplots(specs=[[{'secondary_y': True}]])

fig_2.add_trace(
    go.Scatter(
        x=bike['date'], 
        y=bike['trips_per_day'], 
        name='Daily Bike Rides', 
        marker={'color': 'blue'},
        line=dict(color='blue')
    ), secondary_y=False  
)

fig_2.add_trace(
    go.Scatter(
        x=bike['date'], 
        y=bike['avg_temp'], 
        name='Daily Temperature', 
        marker={'color': 'red'},
        line=dict(color='red')
    ), secondary_y=True  
)

fig_2.update_layout(
    title='Daily Bike Trips and Temperature in NY (2023)', 
    height=800
)

st.plotly_chart(fig_2, use_container_width=True)


## Map ##

path_to_html = 'CitiBike_Bike_Trips.html'

# Read file

with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Citi Bike Trips in NY")
st.components.v1.html(html_data,height=1000)