import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("data/crime_data.csv")

# Fill missing values
df = df.fillna(0)

# Crime columns from your dataset
crime_columns = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']

# Total crime feature
df['total_crime'] = df[crime_columns].sum(axis=1)

# Fake time + location features (for demo ML)
df['hour'] = (df['Year'] * 3) % 24
df['lat'] = (df['Year'] * 1.5) % 90
df['lon'] = (df['Year'] * 2.3) % 180

# Risk labels
df['risk_level'] = 'Low'
df.loc[df['total_crime'] > 3000, 'risk_level'] = 'High'
df.loc[(df['total_crime'] > 1500) & (df['total_crime'] <= 3000), 'risk_level'] = 'Medium'

# Features + target
X = df[['hour', 'lat', 'lon', 'total_crime']]
y = df['risk_level']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Create model folder if not exists
import os
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/safety_model.pkl")

print("✅ Model trained & saved successfully!")

