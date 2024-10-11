import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import datetime
import time
from pydeck.types import String

#########################################################################################
# Load data
st.set_page_config(
    page_title="Map",
    page_icon="👋",
)
st.title('Plotting what is used in the LSTM Model')

DATA_URL = 'c:/Users/Jon/Documents/School/Math 553/Web App Local/pages/heatmap.csv'



########################################################################################
## MAP
# @st.cache_data

def load_data_lstm():
    data = pd.read_csv(DATA_URL)
    
    return data

# Load rows of data into the dataframe.
df_lstm = load_data_lstm()
# Variable for date picker, default to Jan 1st 2020

# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

# Create the scatter plot layer
covidLayer = pdk.Layer(
        "HeatmapLayer",
        data=df_lstm,
        opacity=0.9,
        threshold=0.75,
        get_position=["LongitudeActuals", "LatitudeActuals"],
        aggregation=String('MEAN'),
        get_weight="residual",
        pickable=True
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

# index_range = 10
# index = df_lstm.index.tolist()
# table, act_start = stability_index[metric_to_show]
# running_list = index[table:table+index_range]
# Update the maps and the subheading each day for 90 days
# for i in index[table:]:
    
#     # Update data in map layers
#     covidLayer.data = df_lstm.loc[running_list]

#     # Update the deck.gl map
#     #r.update()

#     # Render the map
#     map.pydeck_chart(r)

#     # Update the heading with current date
#     subheading.subheader("Current Table Row Number: %s out of 681,540" % (act_start))
#     temp_list = running_list[1:]
#     temp_list.append(i)
#     running_list = temp_list
#     act_start+=1
#     # wait 0.1 second before go onto next day
#     time.sleep(0.05)