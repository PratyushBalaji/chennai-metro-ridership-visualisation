# Ridership Visualisation (WIP)

## Info
- Streamlit webapp
- main page will have historical cmrl dashboard (Exact dashboards from cmrl website for Ridership, Parking, PHPDT with slider to go through historical dates)
- create an API that loads the CSVs from github source (so that it is always up to date) and provides multiple getters (ridership on a specific date, PHPDT on a specific date for a certain line, parking at a particular station ID for all time, etc)
- webapp uses API to get data for all the graphs
- apart from main page, will have multiple other visualisations like the phpdt / ridership heatmaps, etc

Essentially serves as a demo for what you can do with the data I am archiving in the other repo.

https://github.com/PratyushBalaji/chennai-metro-ridership-tracker - sister repository / data source

## Visualisations
Planned, existing, and potential visualisations for any given date / date range

### General
- [x] Daily, Hourly, Stationwise ridership (CMRL Dashboard Recreation)
- [x] Daily, Hourly, Stationwise parking (CMRL Dashboard Recreation)
- [x] Daily PHPDT (CMRL Dashboard Recreation)
- [ ] Stationwise Ridership heatmap
- [ ] PHPDT as a heatmap -> folium antpath for up / down and weight for phpdt
- [ ] Historical ridership at a particular station
- [ ] Weekday vs Weekend patterns
- [ ] Commuters vs Casual users patterns (approximated through NCMC vs QR modes)
- [ ] Weather vs ridership (extreme heat or rainfall)
  - Changes in ridership in underground vs elevated stations (AC and sheltered vs non-AC and exposed)
  - Higher ridership because of shelter? Or lower ridership because public transit invites more outdoor mobility? (first / last mile)
  - ONDC usage changes?
- [ ] ONDC usage vs multimodality
  - Multimodal stations like Central have more first/last mile connectivity options so likely have lower relative ONDC usage
  - Non-multimodal stations have more need for end-to-end transport using Uber, Rapido, etc so likely have higher relative ONDC usage

### Case studies
- [ ] Effect of **Egmore railway station redevelopment** on Egmore and other metro stations along affected routes
  - redevelopment from February 22nd to April 5th 2026, analyse ridership at metro stations 2 weeks before and after
  - reduced MRTS schedules (204 trains to 160 trains daily) lead to increased metro ridership (As reported by news articles)
  - account for vadapalani line opening -> increased ridership in the middle of the analysis period
- [ ] Effect of **Poonamallee-Porur-Vadapalani reach operationalisation** on ridership at various metro stations
  - expected opening early march
  - 3 main links from poonamallee to city are :
    - Mount Rd to Guindy
    - Bangalore-Chennai Hwy to Koyambedu
    - Arcot Rd Vadapalani
  - Vadapalani station sees increased ridership from new line. People are now on the metro network earlier and at a new station. What about Guindy and Koyambedu?
  - Koyambedu : largely transitional station => projected lower ridership as people board at vadapalani instead to get on network and bypass fare gates at Koyambedu
  - Guindy : both transitional and destination station => projected higher ridership as MTC users use new line and deboard at Guindy instead of not interacting w/ metro network at all
  - Projected Effect : distribution of embarking ridership b/w koyambedu and vadapalani as network entry points and cumulative disembarking ridership at guindy. Smaller effect on neighbouring stations
  - consider effect of initial porur-vadapalani express service as opposed to local stops after stage 2

### Miscellaneous
- [ ] Ridership during special occasions (public holidays, festivals, Bharath Bandh / strikes, events)
  - February 14/15th A R Rehman concert, CMRL offered event-sponsored QRs for one-time free travel to and from central + extended timings. Ridership on these dates skewed at central, high usage of 'Event QR' payment mode, ridership at odd hours of the day, likely parking impact as well
  - Chepauk cricket match dayw ridership
