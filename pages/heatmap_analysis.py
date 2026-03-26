import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ridership_tracker_api import (
    get_all_station_coordinates,
    get_station_heatmap_data,
    get_station_name_from_code,
    get_station_ridership_dates,
)

st.set_page_config(page_title="Heatmap Analysis", layout="wide")

st.title("Heatmap Analysis")

# default map view state (preserve across slider moves)
if "map_center" not in st.session_state:
    st.session_state.map_center = [13.0827, 80.2707]
if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 11

available_dates = get_station_ridership_dates()

if not available_dates:
    st.warning("No station ridership data available.")
else:
    min_date, max_date = available_dates[0], available_dates[-1]
    st.write("Pick a date span, then scrub the slider to see changes through time.")
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
    date_options = [d for d in available_dates if start_date <= d <= end_date]
    if not date_options:
        st.warning("No data in the selected range.")
    else:
        current_date = st.select_slider(
            "Play through date",
            options=date_options,
            value=date_options[-1],
            format_func=lambda d: d.strftime("%Y-%m-%d"),
            key="date_play_slider",
        )
        date_str = current_date.strftime("%Y-%m-%d")
        readable_date = current_date.strftime("%A, %B %d, %Y")
        st.subheader(f"How was Chennai moving on {readable_date}?")

        coords, max_val, totals = get_station_heatmap_data(date_str)

        if not coords:
            st.warning("No station ridership data available for the selected date.")
        else:
            values = [c[2] for c in coords]
            if values:
                z_cap = pd.Series(values).quantile(0.9)
                if z_cap <= 0:
                    z_cap = max(values)
            else:
                z_cap = 1

            # Build dataframe for Plotly
            data_rows = []
            for lat, lon, val in coords:
                data_rows.append({
                    "lat": lat,
                    "lon": lon,
                    "value": val,
                })
            df = pd.DataFrame(data_rows)

            center_lat, center_lon = st.session_state.map_center
            zoom_level = st.session_state.map_zoom

            # Custom log-like gradient
            gradient = [
                [0.00, "#0d0887"],
                [0.05, "#3b0f70"],
                [0.10, "#6a00a8"],
                [0.20, "#8c2981"],
                [0.35, "#b73779"],
                [0.50, "#d8576b"],
                [0.65, "#ed7953"],
                [0.80, "#fb9f3a"],
                [0.90, "#fdca26"],
                [1.00, "#f0f921"],
            ]

            fig = go.Figure()
            if not df.empty:
                fig.add_densitymapbox(
                    lat=df["lat"],
                    lon=df["lon"],
                    z=df["value"],
                    radius=25,
                    colorscale=gradient,
                    zmin=0,
                    zmax=z_cap,
                    showscale=True,
                )

            # Station markers
            markers = []
            for code, coord in get_all_station_coordinates().items():
                passengers = totals.get(code, 0)
                markers.append({
                    "lat": coord[0],
                    "lon": coord[1],
                    "name": f"{get_station_name_from_code(code)} ({code})",
                    "value": int(passengers),
                    "color": "#003D99" if passengers > 0 else "#555555",
                })
            mdf = pd.DataFrame(markers)
            if not mdf.empty:
                fig.add_scattermapbox(
                    lat=mdf["lat"],
                    lon=mdf["lon"],
                    mode="markers",
                    marker=dict(size=6, color=mdf["color"], opacity=0.9),
                    hovertemplate="%{text}<br>%{customdata} riders<extra></extra>",
                    text=mdf["name"],
                    customdata=mdf["value"],
                    showlegend=False,
                )

            fig.update_layout(
                mapbox_style="carto-darkmatter",
                mapbox_center={"lat": center_lat, "lon": center_lon},
                mapbox_zoom=zoom_level,
                margin=dict(l=0, r=0, t=0, b=0),
                height=720,
            )

            st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
