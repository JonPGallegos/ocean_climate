import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import datetime
import time


#########################################################################################
# Load data
st.set_page_config(
    page_title="Map",
    page_icon="👋",
)
st.title('Plotting what is used in the LSTM Model')

DATA_URL = 'lstm_for_map.csv'

# st.write(df)
############################################################################################

# bar chart 
# filter_data = df[(df['date'] >='2020-04-01') & (df['Country']== 'Australia')].set_index("date")

# st.markdown( "Australia daily Death cases from 1st April 2020")

# st.bar_chart(filter_data[['total_deaths']])


########################################################################################
    #   WIDGETS
# subset_data = df

# ### MULTISELECT
# country_name_input = st.multiselect(
# 'Country name',
# df.groupby('Country').count().reset_index()['Country'].tolist())

# # by country name
# if len(country_name_input) > 0:
#     subset_data = df[df['Country'].isin(country_name_input)]
  
########################################################################################
## linechart

# st.subheader('Comparision of infection growth')

# total_cases_graph  =alt.Chart(subset_data).transform_filter(
#     alt.datum.total_cases > 0  
# ).mark_line().encode(
#     x=alt.X('date', type='nominal', title='Date'),
#     y=alt.Y('sum(total_cases):Q',  title='Confirmed cases'),
#     color='Country',
#     tooltip = 'sum(total_cases)',
# ).properties(
#     width=1500,
#     height=600
# ).configure_axis(
#     labelFontSize=17,
#     titleFontSize=20
# )

# st.altair_chart(total_cases_graph)


########################################################################################
### SELECTBOX widgets
metrics = ['Stable', 'Less Stable', 'Unstable', 'Very Unstable']
#['total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million','new_cases_per_million','total_deaths_per_million','new_deaths_per_million','total_tests','new_tests','total_tests_per_thousand','new_tests_per_thousand']

cols = st.selectbox('Select stability', metrics)

# let's ask the user which column should be used as Index
if cols in metrics:   
    metric_to_show = cols  

stability_index = {'Stable':(1,0), 'Less Stable':(5000,300000), 'Unstable':(10000,500000), 'Very Unstable':(15000, 650000)}


########################################################################################
## MAP
@st.cache_data

def load_data():
    data = pd.read_csv(DATA_URL)
    
    return data

# Load rows of data into the dataframe.
df = load_data()
# Variable for date picker, default to Jan 1st 2020

# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

# Create the scatter plot layer
covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius=metric_to_show,
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],
        tooltip="test test",
    )



# Create the deck.gl map
r = pdk.Deck(
    layers=[covidLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)


# Create a subheading to display current date
subheading = st.subheader("")

# Render the deck.gl map in the Streamlit app as a Pydeck chart 
map = st.pydeck_chart(r)

index_range = 10
index = df.index.tolist()
table, act_start = stability_index[metric_to_show]
running_list = index[table:table+index_range]
# Update the maps and the subheading each day for 90 days
for i in index[table:]:
    
    # Update data in map layers
    covidLayer.data = df.loc[running_list]

    # Update the deck.gl map
    #r.update()

    # Render the map
    map.pydeck_chart(r)

    # Update the heading with current date
    subheading.subheader("Current Table Row Number: %s out of 681,540" % (act_start))
    temp_list = running_list[1:]
    temp_list.append(i)
    running_list = temp_list
    act_start+=1
    # wait 0.1 second before go onto next day
    time.sleep(0.05)