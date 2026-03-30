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

# selecting countries
countries = st.multiselect(label='Pick Countries', 
                            options=df['location'].unique(), 
                            default=['Germany', 'Ireland', 'Italy', 'France', 'Albania'])

# filtering a subset dataframe
country_mask = df['location'].isin(countries)

fig, ax = plt.subplots(figsize = (10, 6))

fig = px.line(
    df,
    x="year",
    y="consumption_in_liters_per_capita",
    #animation_frame='year',
    #animation_group='location',
    color="location",
    color_discrete_sequence = px.colors.qualitative.G10,
    height=600,
    title="Alcohol Consumption Over Time"
)
fig.update_yaxes(rangemode="tozero")
st.plotly_chart(fig)

