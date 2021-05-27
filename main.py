import streamlit as st
import numpy as np
import pgeocode
import pandas as pd
import plotly.express as pt

import plotly.graph_objects as go


st.write("""
# WareYourMask.com
This app finds the probability of contracting COVID-19 base on your Zip code in California
""")
st.sidebar.title("Enter your zip Code")
zip_user_input = st.sidebar.text_input( label="",max_chars=5, value=95618)
zip_user_input = int(zip_user_input)
# reading the CSV file in pandas
htm = pd.read_csv("covid.csv")
# Deleting Colums in CSV file
rae_data =  htm.drop(columns=["Vaccine Equity Metric Quartile", "Mr", "16+ Population", "Redacted"])
# Soring the data with unique counite names
sort_counties = sorted(rae_data.Countie.unique())

county_selected = st.sidebar.multiselect("Select county", sort_counties, default="Yolo")
# Get the info lat and longitude of the Zipcode
nomi = pgeocode.Nominatim('us')
ltng = nomi.query_postal_code(zip_user_input)
latitude = ltng.latitude
longitude = ltng.longitude


@st.cache
def run_init(latitude, longitude):
    df = pd.DataFrame(
        [[latitude,longitude]],
        columns=["latitude", "longitude"])
    return df
st.map(run_init(latitude, longitude), zoom=12)


df_selected_zip = rae_data[(rae_data.Zip.isin([zip_user_input]))]
df_selec = df_selected_zip.drop(columns=["Countie", "Persons Fully Vaccinated", "Persons Partially Vaccinated"])


st.subheader("% of population Vaccinated in your Area")
st.dataframe(df_selec)

# Countie Selected
st.subheader("% of Population Vaccinated in {} countie".format(county_selected[0]))
df_selected_counite = rae_data[(rae_data.Countie.isin(county_selected))]
df_selected_counite = df_selected_counite.drop(columns=["Persons Fully Vaccinated", "Persons Partially Vaccinated"])
st.dataframe(df_selected_counite)

df_selec = df_selec.drop(columns=["Zip"])
astf = df_selec.to_dict('records')
result_dic = astf[0]
labels = list( result_dic.keys())
values = list(result_dic.values())
print(labels)
print(values)




fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3 , pull=[0.1, 0, 0])])


col1, col2 = st.beta_columns(2)
col1.subheader("jhsdasd")
col1.write(fig)












# href = f'<a href="https://data.chhs.ca.gov/dataset/covid-19-vaccine-progress-dashboard-data-by-zip-code/resource/c44b0d65-2fb3-4142-b34c-eff0cd0324c1" >Covid Dataset</a>'
# st.markdown(href, unsafe_allow_html=True)
