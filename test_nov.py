import streamlit as st
import pandas as pd
import os
import glob

st.title("November Data Test")

BASE_PATH = r"c:/Users/anilk/OneDrive/Desktop/LAST_RIDE"
nov_path = os.path.join(BASE_PATH, "NOV")

st.write(f"Looking in: {nov_path}")
st.write(f"Folder exists: {os.path.exists(nov_path)}")

# List all files
files = os.listdir(nov_path)
st.write("Files found:", files)

# Try to load each file
st.subheader("Loading November Files")

# ABV
try:
    abv_file = glob.glob(os.path.join(nov_path, "*abv*.xlsx"))
    st.write(f"ABV file: {abv_file}")
    if abv_file:
        df = pd.read_excel(abv_file[0])
        st.write(f"ABV shape: {df.shape}")
        st.write(f"ABV columns: {list(df.columns)}")
        st.dataframe(df.head())
except Exception as e:
    st.error(f"ABV error: {e}")

# Orders
try:
    orders_file = glob.glob(os.path.join(nov_path, "*orders*.xlsx"))
    st.write(f"Orders file: {orders_file}")
    if orders_file:
        df = pd.read_excel(orders_file[0])
        st.write(f"Orders shape: {df.shape}")
        st.write(f"Orders columns: {list(df.columns)}")
        st.dataframe(df.head())
except Exception as e:
    st.error(f"Orders error: {e}")

# Turnover
try:
    turnover_file = glob.glob(os.path.join(nov_path, "*turnover*.xlsx"))
    st.write(f"Turnover file: {turnover_file}")
    if turnover_file:
        df = pd.read_excel(turnover_file[0])
        st.write(f"Turnover shape: {df.shape}")
        st.write(f"Turnover columns: {list(df.columns)}")
        st.dataframe(df.head())
except Exception as e:
    st.error(f"Turnover error: {e}")

# KPI
try:
    kpi_file = glob.glob(os.path.join(nov_path, "*kpi*.xlsx"))
    st.write(f"KPI file: {kpi_file}")
    if kpi_file:
        df = pd.read_excel(kpi_file[0])
        st.write(f"KPI shape: {df.shape}")
        st.write(f"KPI columns: {list(df.columns)}")
        st.dataframe(df)
except Exception as e:
    st.error(f"KPI error: {e}")

# Products
try:
    items_file = glob.glob(os.path.join(nov_path, "product*.xlsx"))
    st.write(f"Products file: {items_file}")
    if items_file:
        df = pd.read_excel(items_file[0])
        st.write(f"Products shape: {df.shape}")
        st.write(f"Products columns: {list(df.columns)}")
        st.dataframe(df.head())
except Exception as e:
    st.error(f"Products error: {e}")
