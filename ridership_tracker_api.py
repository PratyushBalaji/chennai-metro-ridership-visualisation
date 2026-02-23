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


# PHPDT station order mapping (from start to end of each line)
PHPDT_LINE_STATIONS = {
    1: ["SAP", "SME", "SOT", "SAL", "SGU", "SLM", "SSA", "SCR", "STE", "SGM", "STL", "SLI", "SGE", "SCC", "SHC", "SMA", "SWA", "STC", "STR", "SNW", "STG", "SKP", "STT", "STV", "SWN", "SWD"],
    2: ["SMM", "SAL", "SSI", "SAN", "SVA", "SAR", "SCM", "SKO", "STI", "SAT", "SAE", "SSN", "SPC", "SKM", "SNP", "SEG", "SCC"],
}


def get_phpdt_bar_color(line_num, direction):
    """Get color for PHPDT bars based on line and direction."""
    if line_num == 1:
        # Line 1: Blue base
        if direction == "UP":
            return "#4DA6FF"  # Lighter blue for UP
        else:  # DOWN
            return "#003D99"  # Darker blue for DOWN
    else:  # Line 2
        # Line 2: Green base
        if direction == "UP":
            return "#66d966"  # Lighter green for UP
        else:  # DOWN
            return "#0d7f0d"  # Darker green for DOWN


# payment method display names mapping
PAYMENT_METHOD_DISPLAY_NAMES = {
    "noOfTotal_QR": "Total QR",
    "noOfPaperQR": "Paper QR",
    "noOfONDCQR": "ONDC QR",
    "noOfWhatsAppQR": "WhatsApp QR",
    "noOfRapidoQR": "Rapido QR",
    "noOfPhonePeQR": "PhonePe QR",
    "noOfPaytmQR": "Paytm QR",
    "noOfStaticQR": "Static QR",
    "noOfRedBusQR": "RedBus QR",
    "noOfMobileQR": "Mobile QR",
    "noOfCumtaQR": "Cumta QR",
    "noOfEventQR": "Event QR",
    "noOfJusPayQR": "JusPay QR",
    "noOfPromotionalRideQR": "Promotional QR",
    "noOfMilesKilometersQR": "Miles & Km QR",
    "noOfUberQR": "Uber ONDC",
    "noOfNCMCcard": "Singara Chennai Card",
    "noOfSVP": "Smart Value Pass",
    "noOfCards": "Store Value Card",
    "noOfToken": "Token",
    "noOfTouristCard": "Tourist Card",
    "noOfTripcard": "Trip Card",
    "noOfGroupCard": "Group Card",
}


def format_number(num):
    """Format a number with commas for display."""
    return f"{int(num):,}"


# color scheme for metrics
COLOR_SCHEME = {
    "total": "#0066CC",  # blue
    "closed_loop": "#FF9500",  # orange
    "singara": "#17A2B8",  # teal/turquoise
    "qr": "#9C27B0",  # purple
    "ice": "#8B5A3C",  # brown
    "electric": "#2ca02c",  # green
    "hybrid": "#9C27B0",  # purple
}


def get_payment_methods_for_display(agg_data):
    """
    Extract all payment methods from aggregated data and return as list of (column_name, display_name, value).
    Ordered by value (descending). Excludes headliner ONDC, token, and duplicates.
    """
    methods = []
    exclude_columns = ["Date", "Total", "noOfTotal_QR", "noOfONDCQR", "noOfSVC", "noOfToken"]
    
    for col in agg_data.columns:
        if col not in exclude_columns:
            display_name = PAYMENT_METHOD_DISPLAY_NAMES.get(col, col)
            value = agg_data[col].values[0]
            methods.append((col, display_name, int(value)))
    
    methods.sort(key=lambda x: x[2], reverse=True)
    return methods


def get_payment_method_color(col_name):
    """
    Determine color for a payment method based on its type.
    QR methods -> purple, Singara/NCMC -> teal, Closed loop cards/passes -> orange, others -> gray
    """
    if col_name == "noOfNCMCcard":
        return COLOR_SCHEME["singara"]
    elif col_name == "noOfCards":
        return COLOR_SCHEME["closed_loop"]
    elif col_name.endswith("QR") or col_name == 'noOfSVP':
        return COLOR_SCHEME["qr"]
    else:
        return "#808080" # grey for unrecognised

# parking vehicle type display names mapping
PARKING_COLUMN_DISPLAY_NAMES = {
    "eFourWheeler": "Electric 4-Wheeler",
    "eTwoWheeler": "Electric 2-Wheeler",
    "hFourWheeler": "Hybrid 4-Wheeler",
    "hTwoWheeler": "Hybrid 2-Wheeler",
    "fourWheeler": "4-Wheeler (ICE)",
    "twoWheeler": "2-Wheeler (ICE)",
    "threeWheeler": "3-Wheeler (ICE)",
    "sixWheeler": "6-Wheeler (ICE)",
    "eightWheeler": "8-Wheeler (ICE)",
}


def get_parking_methods_for_display(daily_parking):
    """
    Extract all vehicle types from daily parking data and return as list of (column_name, display_name, value).
    Ordered by value (descending). Excludes total. Calculates 3-wheeler as (threeWheeler - fourWheeler).
    """
    methods = []
    exclude_columns = ["Date", "Total Vehicles"]
    
    # Calculate 3-wheeler separately
    three_wheeler_value = int(daily_parking["threeWheeler"].values[0]) - int(daily_parking["fourWheeler"].values[0])
    
    for col in daily_parking.columns:
        if col not in exclude_columns:
            display_name = PARKING_COLUMN_DISPLAY_NAMES.get(col, col)
            
            # Use calculated value for 3-wheeler
            if col == "threeWheeler":
                value = three_wheeler_value
            else:
                value = int(daily_parking[col].values[0])
            
            methods.append((col, display_name, value))
    
    # sort by value descending
    methods.sort(key=lambda x: x[2], reverse=True)
    return methods


def get_parking_method_color(col_name):
    """
    Determine color for a vehicle type based on its category.
    Electric -> green, Hybrid -> purple, ICE -> brown, others -> gray
    """
    if col_name in ["eFourWheeler", "eTwoWheeler"]:
        return COLOR_SCHEME["electric"]
    elif col_name in ["hFourWheeler", "hTwoWheeler"]:
        return COLOR_SCHEME["hybrid"]
    elif col_name in ["fourWheeler", "twoWheeler", "threeWheeler", "sixWheeler", "eightWheeler"]:
        return COLOR_SCHEME["ice"]
    else:
        return "#808080"  # gray for others