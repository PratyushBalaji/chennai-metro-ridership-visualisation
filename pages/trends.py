import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ridership_tracker_api import (
	get_payment_method_color,
	get_station_fare_modes,
	get_station_options,
	get_station_ridership_between,
	get_station_ridership_dates,
)

st.set_page_config(page_title="Trends & Forecasting", layout="wide")

st.title("Station Ridership by Fare Mode")

available_dates = get_station_ridership_dates()

if not available_dates:
	st.warning("No station ridership data available.")
	st.stop()

min_date, max_date = available_dates[0], available_dates[-1]

col1, col2 = st.columns([2, 1])

with col1:
	selected_range = st.date_input(
		"Date range",
		value=(min_date, max_date),
		min_value=min_date,
		max_value=max_date,
	)
	if not selected_range or len(selected_range) != 2:
		st.warning("Please select a valid date range.")
		st.stop()
	start_date, end_date = selected_range
	if start_date > end_date:
		start_date, end_date = end_date, start_date

with col2:
	station_choices = get_station_options()
	station_names = [name for name, _ in station_choices]
	station_codes = {name: code for name, code in station_choices}
	selected_station_name = st.selectbox("Station", station_names, index=0)
	selected_station_code = station_codes[selected_station_name]

fare_modes = get_station_fare_modes()
fare_mode_map = {display: col for col, display in fare_modes}
fare_mode_labels = list(fare_mode_map.keys())
default_modes = ["Total"] if "Total" in fare_mode_labels else []

selected_modes_display = st.multiselect(
	"Fare modes (lines)",
	options=fare_mode_labels,
	default=default_modes,
)

mode_columns = [fare_mode_map[label] for label in selected_modes_display if label in fare_mode_map]

df = get_station_ridership_between(start_date, end_date, selected_station_code)

if df.empty:
	st.warning("No data for the selected station/date range.")
	st.stop()

day_filter = st.radio(
	"Days",
	options=["All days", "Weekdays only", "Weekends only"],
	index=0,
	horizontal=True,
)

if day_filter != "All days":
	df["dayofweek"] = df["Date"].dt.weekday
	if day_filter == "Weekdays only":
		df = df[df["dayofweek"] < 5]
	else:
		df = df[df["dayofweek"] >= 5]
	df = df.drop(columns=["dayofweek"])
	if df.empty:
		st.warning("No data after applying the day filter.")
		st.stop()

# ensure numeric and aggregate by date to avoid jagged lines from repeated rows
numeric_cols = [col for col in df.columns if col not in ["Date", "Station"]]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df.groupby("Date", as_index=False)[numeric_cols].sum()
df = df.sort_values("Date")

# categorical x labels to avoid gaps when filtering weekdays/weekends
df["DateLabelShort"] = df["Date"].dt.strftime("%a, %b %d")
df["DateLabelFull"] = df["Date"].dt.strftime("%A, %B %d, %Y")
x_labels = df["DateLabelShort"].tolist()
full_labels = df["DateLabelFull"].tolist()

fig = go.Figure()

if "Total" in df.columns:
	fig.add_bar(
		x=x_labels,
		y=df["Total"],
		name="Total",
		marker_color="#0066CC",
		opacity=0.8,
		customdata=full_labels,
		hovertemplate="%{customdata}<br>%{y:.0f} riders<extra></extra>",
	)

for col in mode_columns:
	if col not in df.columns:
		continue
	display = next((d for c, d in fare_modes if c == col), col)
	color = get_payment_method_color(col) if col != "Total" else "#0066CC"
	fig.add_scatter(
		x=x_labels,
		y=df[col],
		mode="lines+markers",
		name=display,
		line=dict(color=color, width=2),
		marker=dict(size=6, color=color),
		customdata=full_labels,
		hovertemplate="%{customdata}<br>%{y:.0f} riders<extra></extra>",
	)

fig.update_layout(
	xaxis_title="Date",
	xaxis_type="category",
	xaxis_categoryorder="array",
	xaxis_categoryarray=x_labels,
	yaxis_title="Ridership",
	legend_title="Fare modes",
	barmode="overlay",
	hovermode="x unified",
	margin=dict(l=40, r=20, t=40, b=40),
)

st.plotly_chart(fig, use_container_width=True)
