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

DATA_URL = 'c:/Users/jonpg/OneDrive/Documents/School/Math 553/Web App Local/pages/heatmap.csv'



########################################################################################
## MAP
# @st.cache_data

def load_data_lstm():
    data = pd.read_csv(DATA_URL)
    
    return data

# Load rows of data into the dataframe.
df_lstm = load_data_lstm()
total = len(df_lstm)
on = st.toggle("Find Best Fit", True)

if on:
    #max is worst so we need to inverse to put the best as the max
    df_lstm.sort_values(by=['residual'], ascending=[False], inplace=True)
    df_lstm['residual'] = df_lstm['residual'] ** -1
else:
    df_lstm.sort_values(by=['residual'], ascending=[True], inplace=True)
    df_lstm['residual'] = df_lstm['residual'] ** 1



lower, upper = st.slider("Select a percent range to include: ", 0, 100, (15, 85))
lower = lower/100
upper = upper/100





df_lstm = df_lstm.iloc[round(lower*total):round(upper*total)]

st.write(f"Count: {len(df_lstm)*100/total}%")

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

st.table()