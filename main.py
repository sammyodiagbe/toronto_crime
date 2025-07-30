import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import folium


crime_data = pd.read_csv("./data/toronto_crime_data.csv")
map_cord = [43.651070, -79.347015]

crime_map = folium.Map(location=map_cord, zoom_start=12)
color_map = {
    "Assault": "blue",
    "Break and Enter": "green",
    "Robbery": "purple",
    "Theft Over": "orange",
    "Auto Theft": "darkred",
    # Add more if needed
}

crime_data.drop(columns=["OBJECTID", "EVENT_UNIQUE_ID", "x", "y", "OCC_DAY", "OCC_YEAR", "OCC_MONTH"], inplace=True)

FEATURES = ["REPORT_DATE", "OCC_DATE", "REPORT_YEAR", "REPORT_MONTH", "REPORT_DOW", "REPORT_HOUR", "OCC_HOUR", "DIVISION", "LOCATION_TYPE", "PREMISES_TYPE", "UCR_CODE", "OFFENCE", "MCI_CATEGORY", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140", "LONG_WGS84", "LAT_WGS84"]

crime_data = crime_data[FEATURES]


crime_data["OCC_DATE"] = pd.to_datetime(crime_data["OCC_DATE"])
crime_data["OCC_YEAR"] = crime_data["OCC_DATE"].dt.year
crime_data["OCC_MONTH"] = crime_data["OCC_DATE"].dt.month
crime_data["OCC_DAY"] = crime_data["OCC_DATE"].dt.day
crime_data["OCC_HOUR"] = crime_data["OCC_DATE"].dt.hour
crime_data["OCC_DOW"] = crime_data["OCC_DATE"].dt.day_of_week

for long, lat, crime_type  in zip(crime_data['LONG_WGS84'],  crime_data['LAT_WGS84'], crime_data['MCI_CATEGORY']):
    folium.CircleMarker(
            location=[lat, long],
            radius=2,
            popup=f"{crime_type}",
            color=color_map.get(crime_type, "gray"),
            fill=True
    ).add_to(crime_map)



# plt.figure(figsize=(12, 6))
# crime_counts = crime_data['MCI_CATEGORY'].value_counts()
# seaborn.barplot(x=crime_counts.values, y=crime_counts.index)
# plt.title('Distribution of Crime Types')
# plt.xlabel('Number of Incidents')
# plt.show()

# yearly_crimes = crime_data.groupby('OCC_YEAR').size()
# plt.figure(figsize=(10, 6))
# yearly_crimes.plot(kind='line', marker='x')
# plt.title('Crime Trends Over Years')
# plt.xlabel('Year')
# plt.ylabel('Number of Crimes')
# plt.show()

crime_map.save("./data/crime_map.html")
print("Exported successfully")

