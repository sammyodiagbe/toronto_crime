import pandas as pd 

crime_data = pd.read_csv("./data/toronto_crime_data.csv")
crime_data.drop(columns=["OBJECTID", "EVENT_UNIQUE_ID", "x", "y"], inplace=True)


print(crime_data.head())


