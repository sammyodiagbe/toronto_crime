import pandas as pd 
import datetime

crime_data = pd.read_csv("./data/toronto_crime_data.csv")
crime_data.drop(columns=["OBJECTID", "EVENT_UNIQUE_ID", "x", "y"], inplace=True)

FEATURES = ["REPORT_DATE", "OCC_DATE", "REPORT_YEAR", "REPORT_MONTH", "REPORT_DOW", "REPORT_HOUR", "OCC_YEAR", "OCC_MONTH", "OCC_DAY", "OCC_HOUR", "DIVISION", "LOCATION_TYPE", "PREMISES_TYPE", "UCR_CODE", "OFFENCE", "MCI_CATEGORY", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140", "LONG_WGS84", "LAT_WGS84"]

crime_data = crime_data[FEATURES]

d_type = (crime_data.dtypes == 'object')

print(d_type)

object_cols = list(d_type[d_type].index)



print(object_cols)


