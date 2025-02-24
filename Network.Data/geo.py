import pandas as pd
import folium
import json
import glob

# Define borough initials mapping
borough_initials = {
    "Barking and Dagenham": "BD",
    "Barnet": "BA",
    "Bexley": "BX",
    "Brent": "BR",
    "Bromley": "BM",
    "Camden": "CA",
    "City of London": "CL",
    "Croydon": "CR",
    "Ealing": "EA",
    "Enfield": "EN",
    "Greenwich": "GR",
    "Hackney": "HA",
    "Hammersmith and Fulham": "HF",
    "Haringey": "HR",
    "Harrow": "HW",
    "Havering": "HV",
    "Hillingdon": "HI",
    "Hounslow": "HO",
    "Islington": "IS",
    "Kensington and Chelsea": "KC",
    "Kingston upon Thames": "KT",
    "Lambeth": "LB",
    "Lewisham": "LE",
    "Merton": "ME",
    "Newham": "NE",
    "Redbridge": "RE",
    "Richmond upon Thames": "RT",
    "Southwark": "SW",
    "Sutton": "SU",
    "Tower Hamlets": "TH",
    "Waltham Forest": "WF",
    "Wandsworth": "WA",
    "Westminster": "WM"
}

# Path to CSV files
file_pattern = "performance_postcode_files/202105_fixed_pc_performance_r01_*.csv"

# List to store DataFrames
df_list = []

# Read all CSV files dynamically and append to list
for file in glob.glob(file_pattern):
    # Extract borough code from filename
    code = file.split("_")[-1].split(".")[0]  # Extracts BD, BA, etc.

    # Find the matching borough name
    borough_name = next((name for name, abbrev in borough_initials.items() if abbrev == code), None)

    if borough_name:
        # Read CSV and assign correct borough name
        df = pd.read_csv(file)
        df["postcode_district"] = borough_name

        # Append DataFrame to list
        df_list.append(df)

# Concatenate all DataFrames into one
df = pd.concat(df_list, ignore_index=True)

# Load the GeoJSON file
with open("london_boroughs.geojson") as f:
    geojson_data = json.load(f)

# Get districts that exist in the dataset
valid_districts = set(df["postcode_district"].unique())

# Filter out boroughs that are NOT in the dataset
geojson_data["features"] = [
    feature for feature in geojson_data["features"]
    if feature["properties"]["name"] in valid_districts
]

# Merge DataFrame data into GeoJSON for Tooltip display
for feature in geojson_data["features"]:
    district = feature["properties"]["name"]
    if district in df["postcode_district"].values:
        row = df[df["postcode_district"] == district].iloc[0]
        feature["properties"]["Median Download Speed"] = row["Median download speed (Mbit/s)"]
        feature["properties"]["Average Download Speed"] = row["Average download speed (Mbit/s)"]
        feature["properties"]["Average data usage (GB)"] = row["Average data usage (GB)"]
        feature["properties"]["Average Download Speed"] = row["Average download speed (Mbit/s)"]


# Create Folium Map centered on London
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# Add Choropleth Layer
folium.Choropleth(
    geo_data=geojson_data,  # Use the filtered GeoJSON
    name="choropleth",
    data=df,
    columns=["postcode_district", "Median download speed (Mbit/s)", "Average data usage (GB)"],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Median Download Speed (Mbit/s) in London",
).add_to(m)

# Add tooltips with Median & Average Download Speed
folium.GeoJson(
    geojson_data,
    name="District Info",
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "Median Download Speed", "Average Download Speed", "Average data usage (GB)"],
        aliases=["District:", "Median Download Speed (Mbps):", "Average Download Speed (Mbps):", "Average data usage (GB)"],
        localize=True,
        sticky=False
    )
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save("london_broadband_map.html")

print("Map saved as london_broadband_map.html - Open in a browser to view.")


# Median download speed (Mbit/s),
# Average download speed (Mbit/s),
# Maximum download speed (Mbit/s),
# Average download speed (Mbit/s) for lines < 10Mbit/s,
# Average download speed (Mbit/s) for lines 10<30Mbit/s,
# Average download speed (Mbit/s) for lines 30<300Mbit/s,
# Average download speed (Mbit/s) for SFBB lines,
# Average download speed (Mbit/s) for UFBB lines,
# Median upload speed (Mbit/s),
# Average upload speed (Mbit/s),
# Maximum upload speed (Mbit/s),
# Average upload speed (Mbit/s) for lines < 10Mbit/s,
# Average upload speed (Mbit/s) for lines 10<30Mbit/s,
# Average upload speed (Mbit/s) for lines 30<300Mbit/s,
# Average upload speed (Mbit/s) for SFBB lines,
# Average upload speed (Mbit/s) for UFBB lines,

# Number of connections < 2 Mbit/s (number of lines),
# Number of connections 2<5 Mbit/s (number of lines),
# Number of connections 5<10 Mbit/s (number of lines),
# Number of connections 10<30 Mbit/s (number of lines),
# Number of connections 30<300 Mbit/s (number of lines),
# Number of connections >= 300 Mbit/s (number of lines),
# Number of connections >= 30 Mbit/s (number of lines),

# Average data usage (GB),
# Median data usage (GB),
# Average data usage (GB) for lines <10Mbits,
# Average data usage (GB) for lines 10<30Mbit/s,
# Average data usage (GB) for lines 30<300Mbit/s,
# Average data usage (GB) for SFBB lines,
# Average data usage (GB) for UFBB lines

