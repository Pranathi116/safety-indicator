import pandas as pd

# Load dataset
df = pd.read_csv("data/crime_data.csv")
df = df.fillna(0)

# Crime columns from your dataset
crime_columns = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']

# Group by State and sum crimes
state_df = df.groupby("State")[crime_columns].sum().reset_index()

# Total crime feature
state_df["total_crime"] = state_df[crime_columns].sum(axis=1)

# Risk labels
state_df["risk_level"] = "Low"
state_df.loc[state_df["total_crime"] > 50000, "risk_level"] = "High"
state_df.loc[
    (state_df["total_crime"] > 20000) & (state_df["total_crime"] <= 50000),
    "risk_level"
] = "Medium"

# Save new CSV
state_df.to_csv("data/state_crime_summary.csv", index=False)

print("✅ State-wise crime summary created!")

