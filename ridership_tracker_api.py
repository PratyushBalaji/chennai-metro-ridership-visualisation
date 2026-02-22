import pandas as pd

# raw data source from repo/main to keep up w daily updates
BASE_URL = "https://raw.githubusercontent.com/PratyushBalaji/chennai-metro-ridership-tracker/refs/heads/main/"

# relative paths to raw url
RIDERSHIP_DAILY_REL_PATH = "Ridership/ChennaiMetro_Daily_Ridership.csv"
RIDERSHIP_HOURLY_REL_PATH = "Ridership/ChennaiMetro_Hourly_Ridership.csv"
RIDERSHIP_STATION_REL_PATH = "Ridership/ChennaiMetro_Station_Ridership.csv"

PARKING_DAILY_REL_PATH = "Parking/ChennaiMetro_Daily_Parking.csv"
PARKING_HOURLY_REL_PATH = "Parking/ChennaiMetro_Hourly_Parking.csv"
PARKING_STATION_REL_PATH = "Parking/ChennaiMetro_Station_Parking.csv"

PHPDT_DAILY_REL_PATH = "PHPDT/ChennaiMetro_Daily_PHPDT.csv"

# data source dict (map category to loaded data)
DATA_SOURCES = {
    "ridership_daily": pd.read_csv(BASE_URL + RIDERSHIP_DAILY_REL_PATH),
    "ridership_hourly": pd.read_csv(BASE_URL + RIDERSHIP_HOURLY_REL_PATH),
    "ridership_station": pd.read_csv(BASE_URL + RIDERSHIP_STATION_REL_PATH),
    "parking_daily": pd.read_csv(BASE_URL + PARKING_DAILY_REL_PATH),
    "parking_hourly": pd.read_csv(BASE_URL + PARKING_HOURLY_REL_PATH),
    "parking_station": pd.read_csv(BASE_URL + PARKING_STATION_REL_PATH),
    "phpdt_daily": pd.read_csv(BASE_URL + PHPDT_DAILY_REL_PATH),
}

# basic getters : csv data by date
def get_aggregate_ridership_on_date(date_str):
    return DATA_SOURCES["ridership_daily"][DATA_SOURCES["ridership_daily"]["Date"] == date_str]


def get_hourly_ridership_on_date(date_str):
    return DATA_SOURCES["ridership_hourly"][DATA_SOURCES["ridership_hourly"]["Date"] == date_str]


def get_station_ridership_on_date(date_str):
    return DATA_SOURCES["ridership_station"][DATA_SOURCES["ridership_station"]["Date"] == date_str]


def get_aggregate_parking_on_date(date_str):
    return DATA_SOURCES["parking_daily"][DATA_SOURCES["parking_daily"]["Date"] == date_str]


def get_hourly_parking_on_date(date_str):
    return DATA_SOURCES["parking_hourly"][DATA_SOURCES["parking_hourly"]["Date"] == date_str]


def get_station_parking_on_date(date_str):
    return DATA_SOURCES["parking_station"][DATA_SOURCES["parking_station"]["Date"] == date_str]


def get_phpdt_ridership_on_date(date_str):
    return DATA_SOURCES["phpdt_daily"][DATA_SOURCES["phpdt_daily"]["Date"] == date_str]

# TO DO : csv data by date range, station name, hour range, etc (ADVANCED FILTERS)

# station code-name mapping
STATION_CODE_TO_NAME = {
    "SWD": "Wimco Nagar Depot",
    "SWN": "Wimco Nagar",
    "STV": "Thiruvotriyur",
    "STT": "Thiruvotriyur Theradi",
    "SKP": "Kaladipet",
    "STG": "Tollgate",
    "SNW": "New Washermenpet",
    "STR": "Tondiarpet",
    "STC": "Thiagaraya College",
    "SWA": "Washermanpet",
    "SMA": "Mannadi",
    "SHC": "High Court",
    "SGE": "Government Estate",
    "SLI": "LIC",
    "STL": "Thousand Lights",
    "SGM": "AG-DMS",
    "STE": "Teynampet",
    "SCR": "Nandanam",
    "SSA": "Saidapet",
    "SLM": "Little Mount",
    "SGU": "Guindy",
    "SOT": "OTA - Nanganallur Road",
    "SME": "Meenambakkam",
    "SAP": "Chennai Airport",
    "SCC": "Chennai Central",
    "SEG": "Egmore",
    "SNP": "Nehru Park",
    "SKM": "Kilpauk",
    "SPC": "Pachaiyappas College",
    "SSN": "Shenoy Nagar",
    "SAE": "Anna Nagar East",
    "SAT": "Anna Nagar Tower",
    "STI": "Thirumangalam",
    "SKO": "Koyambedu",
    "SCM": "CMBT",
    "SAR": "Arumbakkam",
    "SVA": "Vadapalani",
    "SAN": "Ashok Nagar",
    "SSI": "Ekkattuthangal",
    "SAL": "Alandur",
    "SMM": "St. Thomas Mount",
}

STATION_NAME_TO_CODE = {v: k for k, v in STATION_CODE_TO_NAME.items()}


def get_station_name_from_code(code):
    return STATION_CODE_TO_NAME.get(code, code)


def get_station_code_from_name(name):
    return STATION_NAME_TO_CODE.get(name, name)

