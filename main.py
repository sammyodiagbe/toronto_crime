import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn


crime_data = pd.read_csv("./data/toronto_crime_data.csv")

print(crime_data.columns)
crime_data.drop(columns=["OBJECTID", "EVENT_UNIQUE_ID", "x", "y", "OCC_DAY", "OCC_YEAR", "OCC_MONTH"], inplace=True)

FEATURES = ["REPORT_DATE", "OCC_DATE", "REPORT_YEAR", "REPORT_MONTH", "REPORT_DOW", "REPORT_HOUR", "OCC_HOUR", "DIVISION", "LOCATION_TYPE", "PREMISES_TYPE", "UCR_CODE", "OFFENCE", "MCI_CATEGORY", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140", "LONG_WGS84", "LAT_WGS84"]

crime_data = crime_data[FEATURES]


plt.figure(figsize=(12, 6))
crime_counts = crime_data['crime_type'].value_counts()
seaborn.barplot(x=crime_counts.values, y=crime_counts.index)
plt.title('Distribution of Crime Types')
plt.xlabel('Number of Incidents')
plt.show()


