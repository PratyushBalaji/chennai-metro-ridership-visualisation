import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ridership_tracker_api import (
    DATA_SOURCES,
    get_aggregate_ridership_on_date,
    get_hourly_ridership_on_date,
    get_station_ridership_on_date,
    # get_aggregate_parking_on_date,
    # get_hourly_parking_on_date,
    # get_station_parking_on_date,
    # get_phpdt_ridership_on_date,
    get_station_name_from_code,
    format_number,
    get_payment_methods_for_display,
    get_payment_method_color,
    PAYMENT_METHOD_DISPLAY_NAMES,
    COLOR_SCHEME,
)


st.set_page_config(page_title="CMRL Historical Dashboard", layout="wide")

hourly_all = DATA_SOURCES["ridership_hourly"].copy()
hourly_all["Date"] = pd.to_datetime(hourly_all["Date"], errors="coerce")
hourly_all = hourly_all.dropna(subset=["Date"])

if hourly_all.empty:
    st.error("No data available.")
    st.stop()

min_date = hourly_all["Date"].min().date()
max_date = hourly_all["Date"].max().date()

if "selected_date" not in st.session_state:
    st.session_state.selected_date = max_date

st.title("CMRL Historical Dashboard")

col1, col2, _ = st.columns([1, 1, 2])
with col1:
    st.subheader("Select Date")
with col2:
    selected = st.date_input(
        "date",
        value=st.session_state.selected_date,
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )
    st.session_state.selected_date = selected

selected_date_str = st.session_state.selected_date.strftime("%Y-%m-%d") # for api calls
readable_date = pd.to_datetime(selected_date_str).strftime("%A, %B %d, %Y") # for text displaying

tab_ridership, tab_parking, tab_phpdt = st.tabs(["Ridership", "Parking", "PHPDT"])

# RIDERSHIP TAB
with tab_ridership:

    # Daily Stats
    st.subheader(f"Daily Statistics")
    st.caption(f"{readable_date}")
    
    agg_data = get_aggregate_ridership_on_date(selected_date_str)
    
    if not agg_data.empty:
        total_passengers = int(agg_data["Total"].values[0])
        closed_loop = int(agg_data["noOfCards"].values[0])
        singara_card = int(agg_data["noOfNCMCcard"].values[0])
        total_qr = int(agg_data["noOfTotal_QR"].values[0])
        ondc_qr = int(agg_data["noOfONDCQR"].values[0])
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_color = COLOR_SCHEME["total"]
        closed_loop_color = COLOR_SCHEME["closed_loop"]
        singara_color = COLOR_SCHEME["singara"]
        qr_color = COLOR_SCHEME["qr"]
        
        with col1:
            st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Passengers</p>
<p style='color: {total_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_passengers)}</p>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Closed Loop Cards</p>
<p style='color: {closed_loop_color}; font-size: 2.5em; font-weight: bold;'>{format_number(closed_loop)}</p>""", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Singara Chennai Cards</p>
<p style='color: {singara_color}; font-size: 2.5em; font-weight: bold;'>{format_number(singara_card)}</p>""", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total QR (Total ONDC QR : {format_number(ondc_qr)})</p>
<p style='color: {qr_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_qr)}</p>""", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Payment Method Breakdown")
        
        payment_methods = get_payment_methods_for_display(agg_data)
        
        for i in range(0, len(payment_methods), 5):
            cols = st.columns(5)
            for j, (col_name, display_name, value) in enumerate(payment_methods[i:i+5]):
                with cols[j]:
                    method_color = get_payment_method_color(col_name)
                    st.markdown(f"""<div style='text-align: center; padding: 20px 0;'>
<p style='color: white; font-size: 0.95em; margin: 0 0 8px 0;'>{display_name}</p>
<p style='color: {method_color}; font-size: 2em; font-weight: bold; margin: 0;'>{format_number(value)}</p>
</div>""", unsafe_allow_html=True)
    else:
        st.warning(f"No daily aggregate data for {readable_date}.")


    # Hourly Stats
    st.markdown("---")
    st.subheader(f"Hourly Passenger Flow")
    st.caption(f"{readable_date}")

    ridership_day = get_hourly_ridership_on_date(selected_date_str).copy()

    if not ridership_day.empty:
        ridership_day["Time_dt"] = pd.to_datetime(
            ridership_day["Hour"], format="%H:%M", errors="coerce"
        )
        ridership_day = (
            ridership_day.dropna(subset=["Time_dt"])
            .sort_values("Time_dt")
            .reset_index(drop=True)
        )

        payment_methods = [
            col
            for col in ridership_day.columns
            if col not in ["Date", "Hour", "Time_dt", "Total"]
        ]
        
        payment_methods_sorted = sorted(
            payment_methods,
            key=lambda x: ridership_day[x].sum(),
            reverse=True
        )

        fig_hourly = go.Figure()

        fig_hourly.add_trace(
            go.Bar(
                x=ridership_day["Time_dt"],
                y=ridership_day["Total"],
                name="Total Passengers",
                marker_color="lightgray",
                opacity=0.7,
                hovertemplate="<b>Total Passengers</b>: %{y}<extra></extra>",
            )
        )

        for method in payment_methods_sorted:
            fig_hourly.add_trace(
                go.Scatter(
                    x=ridership_day["Time_dt"],
                    y=ridership_day[method],
                    mode="lines",
                    name=method,
                    hovertemplate=f"<b>{method}</b>: %{{y}}<extra></extra>",
                )
            )

        fig_hourly.update_layout(
            # title_text="",
            xaxis_title="Time of Day",
            yaxis_title="Number of Passengers",
            xaxis_tickformat="%H:%M",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
            ),
            height=600,
            margin=dict(t=80, b=120),
        )

        st.plotly_chart(fig_hourly, width="stretch")
    else:
        st.warning(f"No hourly ridership data for {readable_date}.")


    # Station-wise Stats
    st.markdown("---")
    st.subheader(f"Station-wise Passenger Flow")
    st.caption(f"{readable_date}")

    station_day = get_station_ridership_on_date(selected_date_str).copy()

    if not station_day.empty:
        for line_num, line_name, bar_color in [(1, "Line 01 - Blue", "#1f77b4"), (2, "Line 02 - Green", "#2ca02c")]:
            line_data = station_day[station_day["Line"] == line_num].copy()

            if not line_data.empty:
                line_data["Station_Name"] = line_data["Station"].apply(get_station_name_from_code)
                line_data["Station_Display"] = line_data["Station_Name"] + " (" + line_data["Station"] + ")"
                
                payment_methods_station = [
                    col
                    for col in line_data.columns
                    if col not in ["Date", "Line", "Station", "Station_Name", "Station_Display", "Total"]
                ]
                
                # Sort payment methods by total ridership (descending)
                payment_methods_station_sorted = sorted(
                    payment_methods_station,
                    key=lambda x: line_data[x].sum(),
                    reverse=True
                )

                fig_station = go.Figure()

                fig_station.add_trace(
                    go.Bar(
                        x=line_data["Station_Display"],
                        y=line_data["Total"],
                        name="Total Passengers",
                        marker_color=bar_color,
                        opacity=0.7,
                        hovertemplate="Total: %{y}<extra></extra>",
                    )
                )

                for method in payment_methods_station_sorted:
                    fig_station.add_trace(
                        go.Scatter(
                            x=line_data["Station_Display"],
                            y=line_data[method],
                            mode="lines",
                            name=method,
                            hovertemplate=method + ": %{y}<extra></extra>",
                        )
                    )

                fig_station.update_layout(
                    title_text=f"{line_name}",
                    # xaxis_title="Station",
                    yaxis_title="Number of Passengers",
                    hovermode="x unified",
                    xaxis=dict(tickangle=30),
                    legend=dict(
                        x=1.02,
                        y=1,
                        xanchor="left",
                        yanchor="top",
                    ),
                    height=600,
                    margin=dict(t=90, b=150, r=250),
                )

                st.plotly_chart(fig_station, width="stretch")
    else:
        st.warning(f"No station-wise ridership data for {readable_date}.")

    # PARKING TAB
    with tab_parking:
        st.subheader("Daily Parking (Coming Soon)")
        st.info("Daily parking statistics will be displayed here.")

        st.markdown("---")
        st.subheader("Hourly Parking (Coming Soon)")
        st.info("Hourly parking trends will be displayed here.")

        st.markdown("---")
        st.subheader("Station-wise Parking (Coming Soon)")
        st.info("Station-wise parking breakdown will be displayed here.")

    # PHPDT TAB
    with tab_phpdt:
        st.subheader("Peak Hour Per Direction Traffic (Coming Soon)")
        st.info("Corridor-level PHPDT analysis will be displayed here.")
