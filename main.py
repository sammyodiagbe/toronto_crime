import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# --- Load ---
crime_data = pd.read_csv("./data/toronto_crime_data.csv")

# --- Light column pruning early (drop obvious IDs/geom extras you won’t use directly) ---
cols_to_drop = [
    "OBJECTID","EVENT_UNIQUE_ID","x","y","OCC_DOW","DIVISION","LOCATION_TYPE"
]
crime_data = crime_data.drop(columns=[c for c in cols_to_drop if c in crime_data.columns], errors="ignore")

# --- Feature engineering from OCC_DATE ---
crime_data["OCC_DATE"] = pd.to_datetime(crime_data["OCC_DATE"], errors="coerce")
crime_data["OCC_YEAR"]  = crime_data["OCC_DATE"].dt.year
crime_data["OCC_MONTH"] = crime_data["OCC_DATE"].dt.month
crime_data["OCC_DAY"]   = crime_data["OCC_DATE"].dt.day
crime_data["OCC_HOUR"]  = crime_data["OCC_DATE"].dt.hour

# Optional: parse REPORT_DATE too if you want features from it
# crime_data["REPORT_DATE"] = pd.to_datetime(crime_data["REPORT_DATE"], errors="coerce")

# --- Target and features ---
y = crime_data["MCI_CATEGORY"].copy()  # keep strings for readability & metrics output

feature_cols = [
    # numeric/time
    "REPORT_YEAR","REPORT_HOUR","OCC_YEAR","OCC_MONTH","OCC_DAY","OCC_HOUR",
    # numeric-ish
    "UCR_CODE",
    # categorical
    "OFFENCE","PREMISES_TYPE","NEIGHBOURHOOD_158","NEIGHBOURHOOD_140",
    # geo (numerical)
    "LONG_WGS84","LAT_WGS84",
]
# keep only available columns
feature_cols = [c for c in feature_cols if c in crime_data.columns]
X = crime_data[feature_cols]

# --- Column groups ---
numeric_cols = [c for c in feature_cols if c in {"REPORT_YEAR","REPORT_HOUR","OCC_YEAR","OCC_MONTH","OCC_DAY","OCC_HOUR","UCR_CODE","LONG_WGS84","LAT_WGS84"}]
cat_cols = [c for c in feature_cols if c not in numeric_cols]

# --- Preprocess + model pipeline ---
numeric_tf = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
])

cat_tf = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preproc = ColumnTransformer(
    transformers=[
        ("num", numeric_tf, numeric_cols),
        ("cat", cat_tf, cat_cols),
    ]
)

model = RandomForestClassifier(
    n_estimators=300, random_state=42, n_jobs=-1, class_weight=None
)

clf = Pipeline(steps=[
    ("preproc", preproc),
    ("rf", model)
])

# --- Split (stratify preserves class balance) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Train ---
clf.fit(X_train, y_train)

# --- Evaluate ---
y_pred = clf.predict(X_test)
print("classification report")
print(classification_report(y_test, y_pred))
print("confusion matrix")
print(confusion_matrix(y_test, y_pred))
