import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

@st.cache_data
def load_and_preprocess_data():
    # Load the CSV files
    life_expectancy_df = pd.read_csv('lex.csv')
    population_df = pd.read_csv('pop.csv')
    gni_df = pd.read_csv('ny_gnp_pcap_pp_cd.csv')

    # Forward fill missing values
    life_expectancy_df.ffill(inplace=True)
    population_df.ffill(inplace=True)
    gni_df.ffill(inplace=True)

    # Transform each dataframe to tidy data format
    life_expectancy_df = life_expectancy_df.melt(id_vars=["country"], var_name="year", value_name="life_expectancy")
    population_df = population_df.melt(id_vars=["country"], var_name="year", value_name="population")
    gni_df = gni_df.melt(id_vars=["country"], var_name="year", value_name="gni_per_capita")

    # Merge the dataframes
    merged_df = life_expectancy_df.merge(population_df, on=["country", "year"])
    merged_df = merged_df.merge(gni_df, on=["country", "year"])

    return merged_df

# Load and preprocess data
df = load_and_preprocess_data()

# Streamlit UI
st.title("Gapminder Dashboard")

# Year slider
years = df['year'].unique()
selected_year = st.slider('Select Year', min_value=int(years.min()), max_value=int(years.max()), value=int(years.min()))

# Country multiselect
countries = df['country'].unique()
selected_countries = st.multiselect('Select Countries', options=countries, default=countries)

# Filter data based on selections
filtered_df = df[(df['year'] == selected_year) & (df['country'].isin(selected_countries))]

# Logarithmic transformation of GNI per capita
filtered_df['log_gni_per_capita'] = np.log(filtered_df['gni_per_capita'])

# Bubble chart
fig = px.scatter(filtered_df, x='log_gni_per_capita', y='life_expectancy', size='population', color='country',
                 hover_name='country', size_max=60,
                 labels={'log_gni_per_capita': 'Log GNI per Capita', 'life_expectancy': 'Life Expectancy'})

# Set a constant x-axis range for comparability
fig.update_xaxes(range=[filtered_df['log_gni_per_capita'].min() - 1, filtered_df['log_gni_per_capita'].max() + 1])

st.plotly_chart(fig)
