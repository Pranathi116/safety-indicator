import pandas as pd

df = pd.read_csv("data/crime_data.csv")
df = df.fillna(0)

crime_columns = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']


state_df = df.groupby("State")[crime_columns].sum().reset_index()


state_df["total_crime"] = state_df[crime_columns].sum(axis=1)


state_df["risk_level"] = "Low"
state_df.loc[state_df["total_crime"] > 50000, "risk_level"] = "High"
state_df.loc[
    (state_df["total_crime"] > 20000) & (state_df["total_crime"] <= 50000),
    "risk_level"
] = "Medium"


state_df.to_csv("data/state_crime_summary.csv", index=False)

print("✅ State-wise crime summary created!")

