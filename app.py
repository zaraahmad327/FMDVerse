import streamlit as st
import pandas as pd
from Bio import Phylo
import matplotlib.pyplot as plt

st.set_page_config(page_title="FMDV Explorer", layout="wide")
st.title("🦠 FMDV Global Explorer")
st.markdown("Explore Foot-and-Mouth Disease Virus (FMDV) sequences interactively 🌍")

# Load metadata
df = pd.read_excel("fmdv_metadata.xlsx")

# Filters
st.sidebar.header("📊 Filters")
country = st.sidebar.selectbox("Country", ["All"] + sorted(df["Country"].dropna().unique().tolist()))
serotype = st.sidebar.selectbox("Serotype", ["All"] + sorted(df["Serotype"].dropna().unique().tolist()))

filtered = df.copy()
if country != "All":
    filtered = filtered[filtered["Country"] == country]
if serotype != "All":
    filtered = filtered[filtered["Serotype"] == serotype]

st.write(f"Showing {len(filtered)} sequences")

# Charts
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌍 Country Distribution")
    st.bar_chart(df["Country"].value_counts())

with col2:
    st.subheader("🧬 Serotype Distribution")
    st.bar_chart(df["Serotype"].value_counts())

# 🌿 Phylogenetic tree
st.subheader("🌿 Phylogenetic Tree")
try:
    tree = Phylo.read("fmdv_tree_full.nwk", "newick")
    fig = plt.figure(figsize=(10, 10))
    Phylo.draw(tree, do_show=False)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error loading tree: {e}")

# 📈 Outbreak trend (by year)
st.subheader("📈 Outbreak Trends Over Time")
if "Year" in df.columns:
    yearly = df.groupby("Year").size()
    st.line_chart(yearly)
else:
    st.info("No year column found in data.")

# 🔍 Accession search
st.subheader("🔍 Search Accession Number")
query = st.text_input("Enter accession number:")
if query:
    result = df[df["Accession"] == query]
    if not result.empty:
        st.write(result)
    else:
        st.warning("No match found.")
