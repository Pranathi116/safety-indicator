import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib


df = pd.read_csv("data/crime_data.csv")


df = df.fillna(0)


crime_columns = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']

df['total_crime'] = df[crime_columns].sum(axis=1)


df['hour'] = (df['Year'] * 3) % 24
df['lat'] = (df['Year'] * 1.5) % 90
df['lon'] = (df['Year'] * 2.3) % 180


df['risk_level'] = 'Low'
df.loc[df['total_crime'] > 3000, 'risk_level'] = 'High'
df.loc[(df['total_crime'] > 1500) & (df['total_crime'] <= 3000), 'risk_level'] = 'Medium'

X = df[['hour', 'lat', 'lon', 'total_crime']]
y = df['risk_level']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)


import os
os.makedirs("model", exist_ok=True)


joblib.dump(model, "model/safety_model.pkl")

print("✅ Model trained & saved successfully!")

