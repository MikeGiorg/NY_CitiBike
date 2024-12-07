############################################################## CITI BIKE DASHBOARD #############################################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl


####################################################### Initial Setting for the Dashboard ######################################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout = 'wide')
st.title('Citi Bike Strategy Dashboard')

# Define side bar
st.sidebar.title('Selector')
page=st.sidebar.selectbox(
    'Select an aspect of the analysis', 
                          ['Introduction']
                          )


################################################################## Import Data #################################################################################

bike = pd.read_csv(r'../Data/Prepared/dashdata.csv', index_col = 0)
top20 = pd.read_csv(r'../Data/Prepared/top20.csv', index_col = 0)


################################################################ Define the Pages #############################################################################

### Introduction

if page == 'Inroduction':
    st.markdown('The dashboard will help with the expansion problems Citi Bike currently faces')
    st.markdown('Citi Bike currently faces challenges with customers reporting bike unavailability at certain times. This analysis investigates the potential causes of these issues. The dashboard is structured into four sections')
    st.markdown('- Most popular stations')
    st.markdown('- Weather component and bike usage')
    st.markdown('- Interactive map with most common bike trips')
    st.markdown('- Recommendations')
    st.markdown('The 'Selector' dropdown menu on the left allows you to navigate through the various aspects of the analysis that our team explored.')
    myImage=Image.open(../CitiBike.webp) # source: https://citibikenyc.com/how-it-works
    st.image(myImage)
    

## Bar Chart ##

elif page=='Most popular stations':
    
    fig = go.Figure(
        go.Bar(x = top20['start_station'],
               y = top20['value'],
               marker = {'color' : top20['value'], 'colorscale' : 'oranges'} )
               )
    
    fig.update_layout(
        title = '20 Most Popular Bike Stations in NY', 
        xaxis_title = 'Start Stations', 
        yaxis_title = 'Trips', 
        width = 900, 
        height = 600
        )
    
    st.plotly_chart(fig, use_container_width=True)


## Line Chart ##

elif page=='Weather component and bike usage':
    
    fig_2 = make_subplots(specs=[[{'secondary_y': True}]])
    
    fig_2.add_trace(
    go.Scatter(
        x=bike['date'], 
        y=bike['trips_per_day'], 
        name='Daily Bike Rides', 
        marker={'color': '#43AED9'},
        line=dict(color='#43AED9')
    ), secondary_y=False
    )

    fig_2.add_trace(
    go.Scatter(
        x=bike['date'], 
        y=bike['avg_temp'], 
        name='Daily Temperature', 
        marker={'color': '#F2808A'},
        line=dict(color='#F2808A')
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