import streamlit as st

st.set_page_config(page_title="CMRL Dashboard", layout="wide")

st.title("CMRL Analytics Hub")
st.markdown("""
Welcome to the CMRL (Chennai Metro Rail Limited) Analytics Hub. 
This platform provides historical analysis and visualizations of metro ridership, parking, and traffic patterns.

**Navigate using the sidebar to explore:**
- **CMRL Historical Dashboard** - Official dashboard replicas with historical data (WIP)
- **Heatmap Analysis** - Station and corridor heatmap visualizations (TODO)
- **Trends & Forecasting** - Trend analysis and predictions (TODO)

Select a page from the sidebar to begin or scroll down to learn more about this project.
""")

st.markdown("---")

st.markdown("""
### Sister Repository
This project is built on data collected by its sister project, the **[Chennai Metro Ridership Tracker](https://github.com/PratyushBalaji/chennai-metro-ridership-tracker)**, 
which continuously archives historical data from the official CMRL dashboard (https://commuters-data.chennaimetrorail.org/passengerflow). 
The tracker maintains records of daily ridership, parking occupancy, and peak-hour per-direction traffic (PHPDT) across Chennai's metro lines. 
            
Efforts have been put in place to ensure the consistency and validity of the data. The data is unchanged from the official source and is updated daily. 

The historical data and archival project are open-source and available freely for analysis, research, or any derivative works.
""")

st.markdown("---")

st.markdown("""
<p style="font-size: 0.85em;">Copyright © 2026 <b>Pratyush Balaji</b>. This work is licensed under the <a href="https://github.com/PratyushBalaji/chennai-metro-ridership-visualisation/blob/main/LICENSE">MIT License</a>.</p>
""", unsafe_allow_html=True)
