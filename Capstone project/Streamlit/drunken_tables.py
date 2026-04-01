import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

"# **Alcohol Consumption in Europe: Generational Comparison**"
"I'm a Millenial, am I an alcoholic?"

# import data
df = pd.read_csv(
    "/Users/dayaneribeiro/Documents/Spiced/da-capstone-project-dayane-ernesto/Cleaned Sets/Aggregated_Table_Prevalence_Consumption_Abstention.csv"
)
df1 = pd.read_csv("/Users/dayaneribeiro/Documents/Spiced/da-capstone-project-dayane-ernesto/Cleaned Sets/consumption_and_prevalence_2005-2020.csv")

# selecting countries
countries = st.multiselect(label='Pick Countries', 
                            options=df['location'].unique(), 
                            default=['Germany', 'Ireland', 'Italy', 'France', 'Albania'])

# filtering a subset dataframe
#country_mask = df['location'].isin(countries)

df.rename(columns={"consumption_in_liters_per_capita": "Consumption per Capita (Liters)", "location": "Country"}, inplace=True)

df_clean = df.groupby(
    ["Country", "age", "year", "sex"],
    as_index=False
)["Consumption per Capita (Liters)"].mean()

df1["precent_of_prevalence"] = df1["precent_of_prevalence"] * 100
df1.rename(columns={"precent_of_prevalence": "Prevalence", "location": "Country"}, inplace=True)

fig, ax = plt.subplots(figsize = (10, 6))

fig = px.line(
    df_clean,
    x="year",
    y="Consumption per Capita (Liters)",
    #animation_frame='year',
    animation_group='Country',
    color="Country",
    color_discrete_sequence = px.colors.qualitative.G10,
    height=600,
    title="Alcohol Consumption Over Time"
)
fig.update_yaxes(rangemode="tozero")
st.plotly_chart(fig)

countries = ["Germany", "Ireland"]

df_subset = df_clean[df_clean["Country"].isin(countries)]

fig = px.line(
    df_subset,
    x="year",
    y="Consumption per Capita (Liters)",
    color="Country",
    title="Alcohol Consumption Over Time"
)

df1["age_year"] = df1["age"] + " | " + df1["year"].astype(str)

fig = px.choropleth(
    df1,
    locations="Country",
    locationmode="country names",
    color="Prevalence",
    hover_name="Country",
    animation_frame="age_year", 
    color_continuous_scale="RdYlBu",
    title="AUD prevalence by Country and Age"
)
fig.update_geos(
    #scope="europe",
    projection_scale=2.5,
    center={"lat": 54, "lon": 15} 
)

st.plotly_chart(fig)

