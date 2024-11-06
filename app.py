#import libraries
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Interact with Gapminder Data")
#import data

df= pd.read_csv("Data/gapminder_tidy.csv")

#query the data
continent_list = df['continent'].unique()
metric_list = df['metric'].unique()
metric_labels = {"gdpPercap": "GDP Per Capita", "lifeExp":"Average Life Expectancy", "pop":"Population"}

def format_metric(metric_raw):
    return metric_labels[metric_raw]

with st.sidebar:
    st.subheader("Configure the plot")
    continent = st.selectbox("Choose a continent", continent_list)
    metric = st.selectbox("Choose a metric", metric_list, format_func = format_metric)

    
df_filtered = df.query(f"continent == '{continent}' & metric == '{metric}'")
countries_list = df_filtered['country'].unique()
year_min = df_filtered['year'].min()
year_max = df_filtered['year'].max()

years = st.sidebar.slider("What years should be plotted?", year_min, year_max, (year_min, year_max))
countries = st.sidebar.multiselect("Select countries to display in plot", countries_list, default = countries_list)

df_filtered = df_filtered[df_filtered.country.isin(countries)]
#years[0]= min year chosen, years[1] = max year chosen
###look at script for this
df_filtered = df_filtered[(df_filtered.year >= years[0]) & (df_filtered.year <= years[1])]

#make the plot
title = f"{metric_labels[metric]} for countries in {continent}"
fig = px.line(df_filtered, x = "year", y = "value", color = "country", 
              title = title,
             labels = {"value":f"{metric_labels[metric]}"})
st.plotly_chart(fig)

#part 1 - after the plot is displayed, add some text describing the plot
st.markdown(f"**{metric_labels[metric]}** for countries in {continent}")
#st.markdown(f"This plot shows the **{metric_labels[metric]}** from {year[0]} to {year[1]}")

#part 2 - after the plot is displayed, also display the data frame

selected = st.sidebar.checkbox("Display data frame")
if selected:
    st.dataframe(df_filtered)


#selct up slider min and max options from data variable calle dyears
#filter the df_filtered to use only years