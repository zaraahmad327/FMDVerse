import streamlit as st
import pandas as pd
import plotly.express as px
from Bio import SeqIO, Phylo
from io import StringIO
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="FMDV Data Explorer", layout="wide")

st.title("🧬 Foot-and-Mouth Disease Virus (FMDV) Data Explorer")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("/content/fmdv_master_dataset.csv")
    return df

df = load_data()

st.sidebar.header("🔍 Filters")
country_filter = st.sidebar.multiselect("Select Country:", options=sorted(df['Country'].dropna().unique()))
serotype_filter = st.sidebar.multiselect("Select Serotype:", options=sorted(df['Serotype'].dropna().unique()))

filtered_df = df.copy()
if country_filter:
    filtered_df = filtered_df[filtered_df['Country'].isin(country_filter)]
if serotype_filter:
    filtered_df = filtered_df[filtered_df['Serotype'].isin(serotype_filter)]

# --- METADATA OVERVIEW ---
st.subheader("📊 Dataset Overview")
st.write(f"Total sequences: {df.shape[0]}")
st.write(f"Displayed sequences: {filtered_df.shape[0]}")

# --- CHARTS ---
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(filtered_df['Country'].value_counts().head(10),
                  title='Top 10 Countries (Dataset)',
                  labels={'value': 'Number of Sequences', 'index': 'Country'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(filtered_df['Serotype'].value_counts(),
                  title='Serotype Distribution',
                  labels={'value': 'Number of Sequences', 'index': 'Serotype'},
                  color_discrete_sequence=['#f97316'])
    st.plotly_chart(fig2, use_container_width=True)

# --- MAP VISUALIZATION ---
st.subheader("🗺️ Global Spread Map (Dataset-Level)")

# Rough map visualization (will show for known countries)
try:
    map_fig = px.scatter_geo(filtered_df,
                             locations="Country",
                             locationmode="country names",
                             title="FMDV Isolate Distribution",
                             color="Serotype",
                             hover_name="Country")
    st.plotly_chart(map_fig, use_container_width=True)
except Exception as e:
    st.warning("🌍 Some country names may not be geocodable. Clean required.")

# --- DATA TABLE ---
st.subheader("🧾 Filtered Data")
st.dataframe(filtered_df[['Accession', 'Country', 'Serotype', 'Lineage']].head(50))

st.caption("⚠️ Note: This dataset is partial and reflects the available subset analyzed, not the full global dataset.")
