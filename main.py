import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

crime_data = pd.read_csv("./data/toronto_crime_data.csv")
map_cord = [43.651070, -79.347015]
model = RandomForestClassifier(n_estimators=100, random_state=42)
crime_map = folium.Map(location=map_cord, zoom_start=12)
y_pred = crime_data["MCI_CATEGORY"]
color_map = {
    "Assault": "blue",
    "Break and Enter": "green",
    "Robbery": "purple",
    "Theft Over": "orange",
    "Auto Theft": "darkred",
    # Add more if needed
}

encoder.fit(y_pred)

crime_data["OFFENCE"] = encoder.fit_transform(crime_data["OFFENCE"])
crime_data["NEIGHBOURHOOD_158"] = encoder.fit_transform(crime_data["NEIGHBOURHOOD_158"])
crime_data["NEIGHBOURHOOD_140"] = encoder.fit_transform(crime_data["NEIGHBOURHOOD_140"])
crime_data["PREMISES_TYPE"] = encoder.fit_transform(crime_data["PREMISES_TYPE"])
crime_data["MCI_CATEGORY"] = encoder.fit_transform(crime_data["MCI_CATEGORY"])


# this maps the number to the actual text







# crime_data.drop(["OFFENCE", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140"], inplace=True)


marker_cluster = MarkerCluster().add_to(crime_map)



crime_data.drop(columns=["OBJECTID","DIVISION","LOCATION_TYPE", "EVENT_UNIQUE_ID", "x", "y", "OCC_DAY", "OCC_YEAR", "OCC_MONTH", "OCC_DOW", "REPORT_DOW"], inplace=True)

FEATURES = ["REPORT_DATE", "OCC_DATE", "REPORT_YEAR", "REPORT_MONTH", "REPORT_HOUR", "OCC_HOUR", "PREMISES_TYPE", "UCR_CODE", "OFFENCE", "MCI_CATEGORY", "NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140", "LONG_WGS84", "LAT_WGS84"]

crime_data = crime_data[FEATURES]


crime_data["OCC_DATE"] = pd.to_datetime(crime_data["OCC_DATE"])
crime_data["OCC_YEAR"] = crime_data["OCC_DATE"].dt.year
crime_data["OCC_MONTH"] = crime_data["OCC_DATE"].dt.month
crime_data["OCC_DAY"] = crime_data["OCC_DATE"].dt.day
crime_data["OCC_HOUR"] = crime_data["OCC_DATE"].dt.hour

crime_data.drop(columns=["OCC_DATE", "REPORT_DATE", "REPORT_MONTH"], inplace=True)

# for long, lat, crime_type  in zip(crime_data['LONG_WGS84'],  crime_data['LAT_WGS84'], crime_data['MCI_CATEGORY']):
#     folium.CircleMarker(
#             location=[lat, long],
#             radius=2,
#             popup=f"{crime_type}",
#             color=color_map.get(crime_type, "gray"),
#             fill=True
#     ).add_to(crime_map)


x = crime_data.drop(columns=["MCI_CATEGORY"])



train_x, test_x, train_y, test_y = train_test_split(x, y_pred, test_size=0.2, random_state=42)


model.fit(train_x, train_y)

y_predictions = model.predict(test_x)




class_report = classification_report(test_y, y_predictions)
confussion_mat = confusion_matrix(test_y, y_predictions)

print("classification report data")
print(class_report)
print("confussion matrix")
print(confussion_mat)









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

# crime_map.save("./data/crime_map.html")
# print("Exported successfully")

