import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn


crime_data = pd.read_csv("./data/toronto_crime_data.csv")

print(crime_data.columns)
crime_data.drop(columns=["OBJECTID", "EVENT_UNIQUE_ID", "x", "y", "OCC_DAY", "OCC_YEAR", "OCC_MONTH"], inplace=True)

FEATURES = ["REPORT_DATE", "OCC_DATE", "REPORT_YEAR", "REPORT_MONTH", "REPORT_DOW", "REPORT_HOUR", "OCC_HOUR", "DIVISION", "LOCATION_TYPE", "PREMISES_TYPE", "UCR_CODE", "OFFENCE", "MCI_CATEGORY", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140", "LONG_WGS84", "LAT_WGS84"]

crime_data = crime_data[FEATURES]


crime_data["OCC_DATE"] = pd.to_datetime(crime_data["OCC_DATE"])
crime_data["OCC_YEAR"] = crime_data["OCC_DATE"].dt.year
crime_data["OCC_MONTH"] = crime_data["OCC_DATE"].dt.month
crime_data["OCC_DAY"] = crime_data["OCC_DATE"].dt.day
crime_data["OCC_HOUR"] = crime_data["OCC_DATE"].dt.hour
crime_data["OCC_DOW"] = crime_data["OCC_DATE"].dt.day_of_week



# plt.figure(figsize=(12, 6))
# crime_counts = crime_data['MCI_CATEGORY'].value_counts()
# seaborn.barplot(x=crime_counts.values, y=crime_counts.index)
# plt.title('Distribution of Crime Types')
# plt.xlabel('Number of Incidents')
# plt.show()

yearly_crimes = crime_data.groupby('OCC_YEAR').size()
plt.figure(figsize=(10, 6))
yearly_crimes.plot(kind='line', marker='x')
plt.title('Crime Trends Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.show()


