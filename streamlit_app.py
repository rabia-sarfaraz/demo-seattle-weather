# -*- coding: utf-8 -*-

from datetime import datetime
import streamlit as st
import altair as alt
import vega_datasets
import pandas as pd

# ---------------- DATA ----------------
full_df = vega_datasets.data("seattle_weather")

if "custom_df" not in st.session_state:
    st.session_state.custom_df = full_df.copy()

df = st.session_state.custom_df

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Seattle Weather Admin Panel",
    page_icon="🌦️",
    layout="wide",
)

st.title("🌦️ Weather Dashboard + Admin Panel")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("Menu", ["Dashboard", "Admin Panel"])

# =====================================================
# 🔵 ADMIN PANEL
# =====================================================
if menu == "Admin Panel":

    st.subheader("⚙️ Admin Panel")

    date = st.date_input("Date")
    temp_max = st.number_input("Max Temp")
    temp_min = st.number_input("Min Temp")
    wind = st.number_input("Wind Speed")
    precipitation = st.number_input("Precipitation")
    weather = st.selectbox("Weather", ["sun", "rain", "snow", "fog", "drizzle"])

    if st.button("Add Record"):
        new_row = pd.DataFrame({
            "date": [pd.to_datetime(date)],
            "temp_max": [temp_max],
            "temp_min": [temp_min],
            "wind": [wind],
            "precipitation": [precipitation],
            "weather": [weather]
        })

        st.session_state.custom_df = pd.concat([df, new_row], ignore_index=True)
        st.success("Added Successfully ✅")
        st.rerun()

    st.write("### Current Data")
    st.dataframe(df)

# =====================================================
# 🟢 DASHBOARD (FULL ORIGINAL RESTORED)
# =====================================================
else:

    st.subheader("📊 Weather Analytics Dashboard")

    # YEARS FILTER
    YEARS = df["date"].dt.year.unique()
    selected_years = st.pills(
        "Years", YEARS, default=YEARS, selection_mode="multi"
    )

    if not selected_years:
        st.warning("Select at least one year")

    df = df[df["date"].dt.year.isin(selected_years)]

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Max Temp", df["temp_max"].max())
    col2.metric("Min Temp", df["temp_min"].min())
    col3.metric("Avg Wind", df["wind"].mean())

    # ---------------- TEMPERATURE ----------------
    st.write("### Temperature")
    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("date", timeUnit="monthdate"),
            alt.Y("temp_max"),
            alt.Y2("temp_min"),
            alt.Color("date:N", timeUnit="year"),
        )
    )

    # ---------------- WIND ----------------
    st.write("### Wind")
    st.altair_chart(
        alt.Chart(df)
        .mark_line()
        .encode(
            alt.X("date", timeUnit="monthdate"),
            alt.Y("wind"),
            alt.Color("date:N", timeUnit="year"),
        )
    )

    # ---------------- PRECIPITATION ----------------
    st.write("### Precipitation")
    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("date", timeUnit="month"),
            alt.Y("precipitation"),
            alt.Color("date:N", timeUnit="year"),
        )
    )

    # ---------------- MONTHLY BREAKDOWN ----------------
    st.write("### Monthly Breakdown")
    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("month(date):O"),
            alt.Y("count()"),
            alt.Color("weather:N"),
        )
    )

    # ---------------- RAW DATA ----------------
    st.write("### Raw Data")
    st.dataframe(df)