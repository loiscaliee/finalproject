import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 BBCA Forecasting - Moving Average Model")

# Load data
df = pd.read_csv("IDX 2000-2024.csv.gz")

# Filter hanya BBCA
df = df[df["Ticker"] == "BBCA"]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

st.subheader("Data BBCA")
st.write(df.tail())

# Pilih kolom harga
target_col = "Close"

# Pilih window moving average
window = st.number_input("Window Moving Average:", min_value=2, max_value=60, value=7)

# Forecast horizon
horizon = st.number_input("Berapa hari ke depan?", min_value=1, max_value=365, value=30)

# Hitung MA
df["MA"] = df[target_col].rolling(window=window).mean()

st.subheader("Grafik Moving Average")
st.line_chart(df.set_index("Date")[[target_col, "MA"]])

# Forecast: nilai MA terakhir digunakan sebagai prediksi masa depan
last_ma = df["MA"].iloc[-1]
forecast_values = np.repeat(last_ma, horizon)
forecast_index = pd.date_range(start=df["Date"].iloc[-1], periods=horizon+1, freq="D")[1:]

forecast_df = pd.DataFrame({
    "Date": forecast_index,
    "Forecast": forecast_values
})

st.subheader("Forecasting Result")
st.write(forecast_df)

st.subheader("Forecast Plot")
st.line_chart(forecast_df.set_index("Date"))
