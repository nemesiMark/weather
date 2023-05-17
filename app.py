# importo tutte le librerie necessarie
import streamlit as st
import pandas as pd
import toml
from datetime import datetime, date
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import pandas as pd
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import meteostat
import geopy


# implemento la funzione main
def main():

    # file per settare colori di sfondo e testo
    # /
    #with open('.streamlit/config.toml', 'r') as f:
    #    config = toml.load(f)

    st.header("Weather")

    citta = st.text_input("Inserisci il nome della città", value="Bologna")

    geolocator = Nominatim(user_agent="Your_name")
    location = geolocator.geocode(citta)

    data_inizio = st.date_input("Inserisci la data di inizio", date(2019,7,6))

    data_fine = st.date_input("Inserisci la data di fine", date(2023,5,17))

    start = datetime(data_inizio.year, data_inizio.month, data_inizio.day)
    end = datetime(data_fine.year, data_fine.month, data_fine.day)

    cities = {citta:[location.latitude,location.longitude]}

    # Create Point for Vancouver, BC
    city = Point(list(cities.values())[0][0],list(cities.values())[0][1], 20)

    # Get daily data for 2018
    df = Daily(city, start, end)
    df = df.fetch()
    df['city'] = list(cities.keys())[0]

    fig = go.Figure()

    #Actual 
    fig.add_trace(go.Scatter(x = df.index, 
                            y = df['tavg'],
                            mode = "lines",
                            name = "Aveg",
                            line_color='#0000FF',
                            ))
    ##############################################################
    #Predicted 
    fig.add_trace(go.Scatter(x = df.index, 
                            y = df['tmax'],
                            mode = "lines", 
                            name = "Max",
                            line_color='#ff8c00',
                            ))

    ##############################################################
    # adjust layout
    fig.update_layout(title = "Titolo",
                    xaxis_title = "Date",
                    yaxis_title = "Sales",
                    width = 1700,
                    height = 700,
                    )
    ####################################################################
    # zoomming
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=2, label="3y", step="year", stepmode="backward"),
                dict(count=10, label="10y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.add_vline(x=date.today(), line_width=3, line_dash="dash", line_color="red")
    fig.update_layout(width=850)
    st.plotly_chart(fig)
    st.map(pd.DataFrame({'lat' : [location.latitude] , 'lon' : [location.longitude]},columns = ['lat','lon']))

    

# questo modulo sarà eseguito solo se runnato
if __name__ == "__main__":
    main()