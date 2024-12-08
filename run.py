############################################################## CITI BIKE DASHBOARD #############################################################################

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from streamlit_keplergl import keplergl_static
from PIL import Image


####################################################### Initial Setting for the Dashboard ######################################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout = 'wide')
st.title('Citi Bike Strategy Dashboard')

# Define side bar
st.sidebar.title('')
page=st.sidebar.selectbox(
    'Select an aspect of the analysis', 
                          ['Introduction', 'Most Popular Stations',
                           'Weather Impact on Bike Usage', 'Interactive Map with Most Common Trips',
                           'Potential Issues','Recommendations']
                          )


################################################################## Import Data #################################################################################

bike=pd.read_csv(r'Data/Prepared/dashdata.csv', index_col = 0)
top20=pd.read_csv(r'Data/Prepared/top20.csv', index_col = 0)

################################################################ Define the Pages #############################################################################

### Introduction

if page == 'Introduction':
    st.markdown('The dashboard will help with the expansion problems Citi Bike currently faces')
    st.markdown('Citi Bike currently faces challenges with customers reporting bike unavailability at certain times. This analysis investigates the potential causes of these issues. The dashboard is structured into five sections:')
    st.markdown('- Most Popular Stations')
    st.markdown('- Weather Impact on Bike Usage')
    st.markdown('- Interactive Map with Most Common Trips')
    st.markdown('- Potential Issues')
    st.markdown('- Recommendations')
    st.markdown('The dropdown menu on the left allows you to navigate through the various aspects of the analysis that our team explored.')
    
    myImage=Image.open('Data/Original/CB.webp') # source: https://citibikenyc.com/how-it-works 
    st.image(myImage)
    

## Bar Chart ##

elif page=='Most Popular Stations':
    
    fig = go.Figure(
        go.Bar(x = top20['start_station'],
               y = top20['value'],
               marker = {'color' : top20['value'], 'colorscale' : 'blues'} )
               )
    
    fig.update_layout(
        title = '20 Most Popular Bike Stations in NY', 
        xaxis_title = 'Departure Stations', 
        yaxis_title = 'Number of Trips', 
        width = 900, 
        height = 600
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Show in Webpage

    st.markdown('The 20 most frequently used departure stations are situated in Hoboken, NJ, primarily near Hoboken Station and City Hall.')

## Line Chart ##

elif page=='Weather Impact on Bike Usage':

    # Add Filter
    season_filter = st.selectbox('Select Season', ['All', 'Spring', 'Summer', 'Fall', 'Winter'])

    if season_filter != 'All':
        bike = bike[bike['season'] == season_filter]
    
    fig_2=make_subplots(specs=[[{'secondary_y': True}]])
    
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

## Histogram ##

    custom_colors = {
    'casual': '#364573',  
    'member': '#D93240'
    }

    fig_3 = px.histogram(
        bike,
        x='trips_per_day',
        facet_col='membership',  # Split by 'membership'   
        color='membership',   
        title="Daily Trips by Membership Type",
        labels={'trips_per_day': 'Trips per Day', 'membership': 'Membership Type'},
        color_discrete_map=custom_colors
        )
    
    fig_3.update_layout(
        xaxis_title='Trips per Day',
        yaxis_title='Count',
        bargap=0.1
        )

    st.plotly_chart(fig_3, use_container_width=True)     

# Show in Webpage

    st.markdown('Cycling activity appears to generally increase with higher temperatures and decrease with lower temperatures. A clear decline in daily cycling is observed on colder days, indicating that weather significantly impacts overall cycling patterns, with peaks during the summer and dips in the winter.')
    st.markdown('Casual users are less consistent and are more likely to cycle more on good weather days. In contrast, members show more consistent daily cycling, reflecting the steady baseline seen in the first graph, even during colder months. Casual users are more sensitive to seasonal changes, while member activity remains relatively stable throughout the year, but there is still a decrease during extreme cold.')

## Interactive Map ##

elif page=='Interactive Map with Most Common Trips':

    st.components.v1.iframe('https://mikegiorg.github.io/NY_CitiBike/', height=600)

# Show in Webpage
    
    st.markdown('###### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.')
    st.markdown('The route map shows that a significant number of trips are concentrated in the Hoboken area, predominantly consisting of short journeys. However, there are occasional longer trips to specific destinations like NY University or Central Park.')
    st.markdown('The average trip duration is approximately 12 minutes, further supporting the idea that bicycles are primarily used for relatively short distances.')

## Potential Issues ##

elif page=='Potential Issues':

# Group data to plot
    usage=bike.groupby('trip_leng')['ride_id'].nunique().reset_index()

# Custom Colors
    custom_cols=['#D93240', '#364573']

 # Plot Pie    
    fig_4 = go.Figure(
        go.Pie(values=usage['ride_id'],
                       labels=usage['trip_leng'],
                       hole=0.4,
                       marker=dict(colors=custom_cols),
                       textposition='outside')
                       )
    
    fig_4.update_traces(textinfo='percent+label')

    fig_4.update_layout(
        title='Usage of the Bikes',
        height=450
        )
    
    st.plotly_chart(fig_4, use_container_width=True)


# Create interactive boxplot with Plotly
    fig_5 = px.box(
        bike, x="bike_type", 
        y="trip_mins", 
        title="Duration of Trips per Bike Type", 
        labels={"bike_type": "Bike Type", "trip_mins": "Trip Duration in Mins"}
        )
    
    fig_5.update_traces(
        boxpoints='outliers',
        marker=dict(color='#D93240', size=6)  # Change outlier color and size
        )  
    
    fig_5.update_layout(
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        plot_bgcolor="white",
        font=dict(size=10)
        )

# Show the plot in Streamlit
    st.plotly_chart(fig_5, use_container_width=True)
    
# Show in Webpage

    st.markdown('The majority of journeys fall within the maximum duration of 160 minutes. However, a small number of trips: 3,819 in 2023 exceed this limit, with some lasting longer than a full day.')
    st.markdown('This, combined with instances where bikes are shown as docked in the system despite being in use, suggests potential technical issues with the tracking or docking stations.')


else:
    
    st.header('Conclusions and Recommendations')

    st.markdown('- The majority of cycling activity is concentrated around the 20 most frequently used departure stations in Hoboken, NJ, particularly near Hoboken Station and City Hall, indicating a high demand in these areas.')
    st.markdown('- Cycling patterns are heavily influenced by weather, with significant drops in activity on colder days and higher usage during warmer temperatures. This trend is especially pronounced among casual users, who show greater fluctuations based on weather conditions')
    st.markdown('- The average trip duration of 12 minutes indicates that bicycles are primarily used for short-distance travel. This aligns with the our focus on providing quick, efficient transportation for short trips within the city.')
    st.markdown('###### The Next Steps:')
    st.markdown('- Given the concentration of trips around Hoboken, consider expanding bike availability in these areas to meet high demand. This can be done by adjusting bike distribution to ensure availability during peak hours, especially in high-traffic stations.')
    st.markdown('- Given that members show more consistent usage, it might be beneficial to introduce membership-based loyalty programs or discounts. These initiatives could increase year-round usage and improve customer retention among casual users as well.')
    st.markdown('- Investigate and resolve the potential tracking and docking station issues, A thorough audit of the tracking system and regular maintenance of docking stations will help ensure accurate data and improve user experience.')