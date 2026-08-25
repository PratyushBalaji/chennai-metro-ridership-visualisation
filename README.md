# Ridership Visualisation (WIP)

## This page is now live!
This project is now live on streamlit and linked to this repository, so changes here will reflect in real-time. The API directly fetches the most up-to-date information from the ridership archive project, without any manual intervention. Although it barely scratches the surface of everything I want to put up, this work-in-progress deployment currently serves as a proof of concept. Any and all suggestions / issues / discussions / contributions are welcome!

Although streamlit is an extremely rudimentary way of demonstrating the sheer amount of inferences we can make from commuter data, it is merely a stepping stone in the grand scheme of this project. The goal isn't for people to flock to my website, but for people to get inspired by or educated about the use of publicly available data! 

If simple markdown rendering of plotly graphs can show so much, imagine the potential!

This project is for the commuter, the train-nerd, the urban planner, the [Everyman](https://en.wikipedia.org/wiki/Everyman).

[chennai-metro.streamlit.app](https://chennai-metro.streamlit.app)

## Info
- Streamlit webapp
- main page will have historical cmrl dashboard (Exact dashboards from cmrl website for Ridership, Parking, PHPDT with slider to go through historical dates)
- create an API that loads the CSVs from github source (so that it is always up to date) and provides multiple getters (ridership on a specific date, PHPDT on a specific date for a certain line, parking at a particular station ID for all time, etc)
- webapp uses API to get data for all the graphs
- apart from main page, will have multiple other visualisations like the phpdt / ridership heatmaps, etc

Essentially serves as a demo for what you can do with the data I am archiving in the other repo.

https://github.com/PratyushBalaji/chennai-metro-ridership-tracker - sister repository / data source

## Why does this project exist?
This table speaks for itself :

| Cities with Operational Metro Systems | Cities with Public Metro Ridership Statistics | Cities with Historical Ridership Statistics |
| - | - | - |
| Agra <br>Ahmedabad <br>Bengaluru <br>Bhopal <br>Chennai <br>Delhi <br>Gurgaon <br>Hyderabad <br>Indore <br>Jaipur <br>Kanpur <br>Kochi <br>Kolkata <br>Lucknow <br>Meerut <br>Mumbai <br>Nagpur <br>Navi Mumbai <br>Noida <br>Patna <br>Pune <br>Surat | Bengaluru (though inconsistent) <br> Chennai | |

This table will be updated through the project's lifespan. If it no longer justifies this project's existence, either the goal was met, or every metro system in India is no longer operational. Hopefully its the former :)

## Visualisations
Planned, existing, and potential visualisations for any given date / date range

### General
- [x] Daily, Hourly, Stationwise ridership (CMRL Dashboard Recreation)
- [x] Daily, Hourly, Stationwise parking (CMRL Dashboard Recreation)
- [x] Daily PHPDT (CMRL Dashboard Recreation)
- [x] Stationwise Ridership heatmap
- [ ] PHPDT as a heatmap -> folium antpath for up / down and weight for phpdt
- [x] Historical ridership at a particular station
- [ ] Weekday vs Weekend patterns
- [ ] Commuters vs Casual users patterns (approximated through NCMC vs QR modes)
- [ ] Weather vs ridership (extreme heat or rainfall)
  - Changes in ridership in underground vs elevated stations (AC and sheltered vs non-AC and exposed)
  - Higher ridership because of shelter? Or lower ridership because public transit invites more outdoor mobility? (first / last mile)
  - ONDC usage changes?
- [ ] ONDC usage vs multimodality
  - Multimodal stations like Central have more first/last mile connectivity options so likely have lower relative ONDC usage
  - Non-multimodal stations have more need for end-to-end transport using Uber, Rapido, etc so likely have higher relative ONDC usage
- [ ] PHPDT vs Same Hour Parking Flow to analyse commute patterns

### Case studies
- [ ] Effect of **Egmore railway station redevelopment** on Egmore and other metro stations along affected routes
  - redevelopment from February 22nd to April 5th 2026, analyse ridership at metro stations 2 weeks before and after
  - reduced schedules (204 trains to 160 trains daily) lead to increased metro ridership (As reported by news articles)
  - account for vadapalani line opening -> increased ridership in the middle of the analysis period
- [ ] Effect of **Poonamallee-Porur-Vadapalani reach operationalisation** on ridership at various metro stations
  - expected opening early march
  - 3 main links from poonamallee to city are :
    - Mount Rd to Guindy
    - Bangalore-Chennai Hwy to Koyambedu
    - Arcot Rd to Vadapalani
  - Vadapalani station sees increased ridership from new line. People are now on the metro network earlier and at a new station. Existing Arcot rd bus users switch to metro for speed => transfer station which may not reflect in ridership stats but will in PHPDT on yellow & green lines. What about Guindy and Koyambedu?
  - Koyambedu : largely transitional station => projected lower ridership as people board/transfer at vadapalani instead to get on network and bypass fare gates at Koyambedu
  - Guindy : both transitional and destination station => projected higher ridership as MTC users use new line and deboard at Guindy instead of not interacting w/ metro network at all. 
  - Projected Effect : distribution of embarking ridership b/w koyambedu and vadapalani as network entry points and cumulative disembarking ridership at guindy. Smaller effect on neighbouring stations
  - consider effect of initial porur-vadapalani express service as opposed to local stops after stage 2
- [ ] Effect of **Velachery - St Thomas Mount suburban extension** on St Thomas Mount and green line ridership
  - 5km extension that adds another metro-mrts interchange
  - Operationalised on 14 March 2026
  - New direct beach route via mrts from St Thomas Mount via Velachery
  - In far future gauge impact of yellow line phase 2 to lighthouse which acts as alternative direct bypass to beach

### Miscellaneous
- [ ] Ridership during special occasions (public holidays, festivals, Bharath Bandh / strikes, events)
  - February 14/15th A R Rehman concert, CMRL offered event-sponsored QRs for one-time free travel to and from central + extended timings. Ridership on these dates skewed at central, high usage of 'Event QR' payment mode, ridership at odd hours of the day, likely parking impact as well
  - March 7th Hiphop Tamizha concert, event-sponsored QRs for one-time round trip at nandanam station + extended timings at central for transfers
  - Chepauk cricket match day ridership
- [ ] CMRL smart card usage over the years since NCMC introduction (deprecation), usage drop after cancellation announcement, usage after May 1 (obsoletion)
