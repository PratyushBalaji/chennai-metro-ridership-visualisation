import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ridership_tracker_api import (
    DATA_SOURCES,
    get_aggregate_ridership_on_date,
    get_hourly_ridership_on_date,
    get_station_ridership_on_date,
    get_aggregate_parking_on_date,
    get_hourly_parking_on_date,
    get_station_parking_on_date,
    get_phpdt_ridership_on_date,
    get_station_name_from_code,
    format_number,
    get_payment_methods_for_display,
    get_payment_method_color,
    get_parking_methods_for_display,
    get_parking_method_color,
    get_phpdt_bar_color,
    PAYMENT_METHOD_DISPLAY_NAMES,
    PARKING_COLUMN_DISPLAY_NAMES,
    PHPDT_LINE_STATIONS,
    COLOR_SCHEME,
)


st.set_page_config(page_title="CMRL Historical Dashboard", layout="wide")

line_colors = px.colors.qualitative.Bold

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

col1, col2, _ = st.columns([1, 1, 4])
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
            st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total QR (Total ONDC : {format_number(ondc_qr)})</p>
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

        for idx, method in enumerate(payment_methods_sorted):
            # Black outline
            fig_hourly.add_trace(
                go.Scatter(
                    x=ridership_day["Time_dt"],
                    y=ridership_day[method],
                    mode="lines",
                    name=method,
                    line=dict(shape="spline", color="black", width=3.5),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            # Colored line on top
            fig_hourly.add_trace(
                go.Scatter(
                    x=ridership_day["Time_dt"],
                    y=ridership_day[method],
                    mode="lines",
                    name=method,
                    line=dict(shape="spline", color=line_colors[idx % len(line_colors)], width=2.5),
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

                for idx, method in enumerate(payment_methods_station_sorted):
                    # Black outline
                    fig_station.add_trace(
                        go.Scatter(
                            x=line_data["Station_Display"],
                            y=line_data[method],
                            mode="lines",
                            name=method,
                            line=dict(shape="spline", color="black", width=3.5),
                            hoverinfo="skip",
                            showlegend=False,
                        )
                    )
                    # Colored line on top
                    fig_station.add_trace(
                        go.Scatter(
                            x=line_data["Station_Display"],
                            y=line_data[method],
                            mode="lines",
                            name=method,
                            line=dict(shape="spline", color=line_colors[idx % len(line_colors)], width=2.5),
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
        # Daily Stats
        st.subheader(f"Daily Statistics")
        st.caption(f"{readable_date}")
        
        parking_data = get_aggregate_parking_on_date(selected_date_str)
        
        if not parking_data.empty:
            total_vehicles = int(parking_data["Total Vehicles"].values[0])
            
            # split by fuel type
            # Note: threeWheeler is combined 3 & 4-wheelers, so 3-wheeler = threeWheeler - fourWheeler
            four_wheeler = int(parking_data["fourWheeler"].values[0])
            three_wheeler = int(parking_data["threeWheeler"].values[0]) - four_wheeler
            two_wheeler = int(parking_data["twoWheeler"].values[0])
            six_wheeler = int(parking_data["sixWheeler"].values[0])
            eight_wheeler = int(parking_data["eightWheeler"].values[0])
            
            electric_cols = ["eFourWheeler", "eTwoWheeler"]
            hybrid_cols = ["hFourWheeler", "hTwoWheeler"]
            
            total_ice = three_wheeler + four_wheeler + two_wheeler + six_wheeler + eight_wheeler
            total_electric = sum([int(parking_data[col].values[0]) for col in electric_cols if col in parking_data.columns])
            total_hybrid = sum([int(parking_data[col].values[0]) for col in hybrid_cols if col in parking_data.columns])
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_color = COLOR_SCHEME["total"]
            ice_color = COLOR_SCHEME["ice"]
            electric_color = COLOR_SCHEME["electric"]
            hybrid_color = COLOR_SCHEME["hybrid"]
            
            with col1:
                st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Vehicles</p>
<p style='color: {total_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_vehicles)}</p>""", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total ICE Vehicles</p>
<p style='color: {ice_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_ice)}</p>""", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Electric</p>
<p style='color: {electric_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_electric)}</p>""", unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""<p style='color: white; font-size: 1.5em;'>Total Hybrid</p>
<p style='color: {hybrid_color}; font-size: 2.5em; font-weight: bold;'>{format_number(total_hybrid)}</p>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Vehicle Type Breakdown")
            
            parking_methods = get_parking_methods_for_display(parking_data)
            
            for i in range(0, len(parking_methods), 5):
                cols = st.columns(5)
                for j, (col_name, display_name, value) in enumerate(parking_methods[i:i+5]):
                    with cols[j]:
                        method_color = get_parking_method_color(col_name)
                        st.markdown(f"""<div style='text-align: center; padding: 20px 0;'>
<p style='color: white; font-size: 0.95em; margin: 0 0 8px 0;'>{display_name}</p>
<p style='color: {method_color}; font-size: 2em; font-weight: bold; margin: 0;'>{format_number(value)}</p>
</div>""", unsafe_allow_html=True)
        else:
            st.warning(f"No daily parking data for {readable_date}.")

        st.markdown("---")
        st.subheader(f"Hourly Parking")
        st.caption(f"{readable_date}")

        parking_hourly = get_hourly_parking_on_date(selected_date_str).copy()

        if not parking_hourly.empty:
            parking_hourly["Time_dt"] = pd.to_datetime(
                parking_hourly["Hour"], format="%H:%M", errors="coerce"
            )
            parking_hourly = (
                parking_hourly.dropna(subset=["Time_dt"])
                .sort_values("Time_dt")
                .reset_index(drop=True)
            )

            vehicle_types = [
                col
                for col in parking_hourly.columns
                if col not in ["Date", "Hour", "Time_dt", "Total Vehicles", "General Parking"]
            ]
            
            vehicle_types_sorted = sorted(
                vehicle_types,
                key=lambda x: parking_hourly[x].sum(),
                reverse=True
            )

            fig_parking_hourly = go.Figure()

            fig_parking_hourly.add_trace(
                go.Bar(
                    x=parking_hourly["Time_dt"],
                    y=parking_hourly["Total Vehicles"],
                    name="Total Vehicles",
                    marker_color="lightgray",
                    opacity=0.7,
                    hovertemplate="<b>Total Vehicles</b>: %{y}<extra></extra>",
                )
            )

            for idx, vehicle_type in enumerate(vehicle_types_sorted):
                # Black outline
                fig_parking_hourly.add_trace(
                    go.Scatter(
                        x=parking_hourly["Time_dt"],
                        y=parking_hourly[vehicle_type],
                        mode="lines",
                        name=vehicle_type,
                        line=dict(shape="spline", color="black", width=3.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )
                # Colored line on top
                fig_parking_hourly.add_trace(
                    go.Scatter(
                        x=parking_hourly["Time_dt"],
                        y=parking_hourly[vehicle_type],
                        mode="lines",
                        name=vehicle_type,
                        line=dict(shape="spline", color=line_colors[idx % len(line_colors)], width=2.5),
                        hovertemplate=f"<b>{vehicle_type}</b>: %{{y}}<extra></extra>",
                    )
                )

            fig_parking_hourly.update_layout(
                xaxis_title="Time of Day",
                yaxis_title="Number of Vehicles",
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

            st.plotly_chart(fig_parking_hourly, use_container_width=True)
        else:
            st.warning(f"No hourly parking data for {readable_date}.")

        st.markdown("---")
        st.subheader("Station-wise Parking")
        st.caption(f"{readable_date}")

        station_parking = get_station_parking_on_date(selected_date_str).copy()

        if not station_parking.empty:
            for line_num, line_name, bar_color in [("01", "Line 01 - Blue", "#1f77b4"), ("02", "Line 02 - Green", "#2ca02c")]:
                line_data = station_parking[station_parking["Line"].astype(str).str.zfill(2) == line_num].copy()

                if not line_data.empty:
                    line_data["Station_Name"] = line_data["Station"].apply(get_station_name_from_code)
                    line_data["Station_Display"] = line_data["Station_Name"] + " (" + line_data["Station"] + ")"
                    
                    vehicle_types_station = [
                        col
                        for col in line_data.columns
                        if col not in ["Date", "Line", "Station", "Station_Name", "Station_Display", "Total Vehicles", "General Parking", "Eight Wheleer"]
                    ]
                    
                    # Sort vehicle types by total parking (descending)
                    vehicle_types_station_sorted = sorted(
                        vehicle_types_station,
                        key=lambda x: line_data[x].sum(),
                        reverse=True
                    )

                    fig_station_parking = go.Figure()

                    fig_station_parking.add_trace(
                        go.Bar(
                            x=line_data["Station_Display"],
                            y=line_data["Total Vehicles"],
                            name="Total Vehicles",
                            marker_color=bar_color,
                            opacity=0.7,
                            hovertemplate="Total: %{y}<extra></extra>",
                        )
                    )

                    for idx, vehicle_type in enumerate(vehicle_types_station_sorted):
                        # Black outline
                        fig_station_parking.add_trace(
                            go.Scatter(
                                x=line_data["Station_Display"],
                                y=line_data[vehicle_type],
                                mode="lines",
                                name=vehicle_type,
                                line=dict(shape="spline", color="black", width=3.5),
                                hoverinfo="skip",
                                showlegend=False,
                            )
                        )
                        # Colored line on top
                        fig_station_parking.add_trace(
                            go.Scatter(
                                x=line_data["Station_Display"],
                                y=line_data[vehicle_type],
                                mode="lines",
                                name=vehicle_type,
                                line=dict(shape="spline", color=line_colors[idx % len(line_colors)], width=2.5),
                                hovertemplate=vehicle_type + ": %{y}<extra></extra>",
                            )
                        )

                    fig_station_parking.update_layout(
                        title_text=f"{line_name}",
                        yaxis_title="Number of Vehicles",
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

                    st.plotly_chart(fig_station_parking, use_container_width=True)
        else:
            st.warning(f"No station-wise parking data for {readable_date}.")

    # PHPDT TAB
    with tab_phpdt:
        st.subheader("Peak Hour Per Direction Traffic (PHPDT)")
        st.caption(f"{readable_date}")

        display_mode = st.radio(
            "Display",
            ["Bars + Lines", "Bars only", "Lines only"],
            index=0,
            horizontal=True,
            help="Switch between bar view, line view, or both for PHPDT",
        )

        show_bars = display_mode in ["Bars + Lines", "Bars only"]
        show_lines = display_mode in ["Bars + Lines", "Lines only"]
        line_showlegend = display_mode == "Lines only"

        phpdt_day = get_phpdt_ridership_on_date(selected_date_str)

        if phpdt_day.empty:
            st.warning(f"No PHPDT data available for {readable_date}.")
        else:
            # Process each line
            for line_num in [1, 2]:
                line_phpdt = phpdt_day[phpdt_day["Line"] == line_num].copy()

                if line_phpdt.empty:
                    continue

                # Separate UP and DOWN directions
                up_data = line_phpdt[line_phpdt["Direction"] == "UP"].copy()
                down_data = line_phpdt[line_phpdt["Direction"] == "DOWN"].copy()

                # Get station order for this line
                station_order = PHPDT_LINE_STATIONS.get(line_num, [])
                station_names = [get_station_name_from_code(code) for code in station_order]
                station_display = [f"{name} ({code})" for name, code in zip(station_names, station_order)]
                line_start_name = station_names[0] if station_names else ""
                line_end_name = station_names[-1] if station_names else ""
                line_start_code = station_order[0] if station_order else ""
                line_end_code = station_order[-1] if station_order else ""

                # Build corridor data - SEPARATE labels for UP and DOWN
                bar_positions = []  # x position for bars (between stations)
                up_corridor_values = []
                down_corridor_values = []
                up_corridor_labels = []  # UP shows forward direction
                down_corridor_labels = []  # DOWN shows reverse direction

                for i in range(len(station_order) - 1):
                    from_station = station_order[i]
                    to_station = station_order[i + 1]

                    # Bar position is between station i and i+1
                    bar_pos = i + 0.5
                    bar_positions.append(bar_pos)

                    # UP corridor: from_station → to_station
                    up_label = f"{station_names[i]} → {station_names[i + 1]}"
                    up_row = up_data[(up_data["Start Station"] == from_station) & (up_data["End Station"] == to_station)]
                    up_val = up_row["PHPDT"].values[0] if not up_row.empty else 0
                    up_corridor_values.append(up_val)
                    up_corridor_labels.append(up_label)

                    # DOWN corridor: to_station → from_station (REVERSED!)
                    down_label = f"{station_names[i + 1]} → {station_names[i]}"  # Reverse for DOWN
                    down_row = down_data[(down_data["Start Station"] == to_station) & (down_data["End Station"] == from_station)]
                    down_val = down_row["PHPDT"].values[0] if not down_row.empty else 0
                    down_corridor_values.append(down_val)
                    down_corridor_labels.append(down_label)

                # Get peak hours
                up_peak_hour = f"{up_data['Start Hour'].values[0]}-{up_data['End Hour'].values[0]}" if not up_data.empty else "N/A"
                down_peak_hour = f"{down_data['Start Hour'].values[0]}-{down_data['End Hour'].values[0]}" if not down_data.empty else "N/A"

                # Create Plotly figure
                fig_phpdt = go.Figure()

                # Add UP direction bars (positioned between stations)
                up_legend_name = f"UP ({up_peak_hour}) ({line_start_code}-{line_end_code})"
                down_legend_name = f"DOWN ({down_peak_hour}) ({line_end_code}-{line_start_code})"

                if show_bars:
                    fig_phpdt.add_trace(
                        go.Bar(
                            x=bar_positions,
                            y=up_corridor_values,
                            name=up_legend_name,
                            marker_color=get_phpdt_bar_color(line_num, "UP"),
                            hovertemplate="<b>%{customdata}</b><br>UP Passengers: %{y}<br>Peak: " + up_peak_hour + "<extra></extra>",
                            customdata=up_corridor_labels,
                            legendgroup="up",
                            showlegend=True,
                        )
                    )

                # Add DOWN direction bars (positioned between stations)
                if show_bars:
                    fig_phpdt.add_trace(
                        go.Bar(
                            x=bar_positions,
                            y=down_corridor_values,
                            name=down_legend_name,
                            marker_color=get_phpdt_bar_color(line_num, "DOWN"),
                            hovertemplate="<b>%{customdata}</b><br>DOWN Passengers: %{y}<br>Peak: " + down_peak_hour + "<extra></extra>",
                            customdata=down_corridor_labels,
                            legendgroup="down",
                            showlegend=True,
                        )
                    )

                # Smooth lines tracing the bars (no extra legend entries)
                if show_lines:
                    fig_phpdt.add_trace(
                        go.Scatter(
                            x=bar_positions,
                            y=up_corridor_values,
                            mode="lines",
                            name=up_legend_name,
                            line=dict(shape="spline", color=get_phpdt_bar_color(line_num, "UP"), width=2),
                            hovertemplate="<b>%{customdata}</b><br>UP Passengers: %{y}<br>Peak: " + up_peak_hour + "<extra></extra>",
                            customdata=up_corridor_labels,
                            showlegend=line_showlegend,
                            legendgroup="up",
                        )
                    )

                if show_lines:
                    fig_phpdt.add_trace(
                        go.Scatter(
                            x=bar_positions,
                            y=down_corridor_values,
                            mode="lines",
                            name=down_legend_name,
                            line=dict(shape="spline", color=get_phpdt_bar_color(line_num, "DOWN"), width=2),
                            hovertemplate="<b>%{customdata}</b><br>DOWN Passengers: %{y}<br>Peak: " + down_peak_hour + "<extra></extra>",
                            customdata=down_corridor_labels,
                            showlegend=line_showlegend,
                            legendgroup="down",
                        )
                    )

                # Set x-axis to show station names at integer positions
                station_positions = list(range(len(station_names)))
                
                fig_phpdt.update_layout(
                    title_text=f"Line {line_num} - {'Blue' if line_num == 1 else 'Green'} Line between {line_start_name} and {line_end_name}",
                    yaxis_title="Peak Hour Passengers",
                    yaxis=dict(autorange=True, rangemode="tozero"),
                    barmode="group",
                    hovermode="x unified",
                    xaxis=dict(
                        type="linear",
                        tickmode="array",
                        tickvals=station_positions,
                        ticktext=station_display,
                        tickangle=30,
                        zeroline=False,
                        range=[-0.5, len(station_positions) - 0.5],
                    ),
                    legend=dict(
                        orientation="h",
                        x=0.5,
                        xanchor="center",
                        y=-0.3,
                        yanchor="top",
                    ),
                    height=600,
                    margin=dict(t=90, b=200, r=40, l=40),
                )

                st.plotly_chart(fig_phpdt, use_container_width=True)
