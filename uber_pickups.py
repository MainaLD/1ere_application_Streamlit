from cgi import test
import streamlit as st
import pandas as pd
import numpy as np

# Tritre de l'application
st.title('Uber pickups in NYC')

# une fonction pour charger les données
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# load_datas, ancienne fonction simple, télécharge certaines données, les place dans une trame de données Pandas et convertit la colonne date (texte) en datetime
# (nrows) = nb de lignes à charger dans la dataframe

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#  tester et observer le rendu
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")


# Inspecter les données brutes // Afficher la dataframe
# st.subheader('Raw data') 
# st.write(data) // ou // # st.dataframe(data)
# ligne Remplacer par un bouton pour basculer les données :
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#  Dessiner un histogramme
# NumPy pour générer un histogramme qui décompose les heures de ramassage par heure
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)


# Tracer des données sur une carte 
# st.subheader('Map of all pickups')
# st.map(data)

#  => remplacer par :
# hour_to_filter = 17 
# Code en dur remplacer par un  Filtre des résultats avec un curseur
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# Si visualisation de données carto : st.pydeck_chart
st.map(filtered_data)








