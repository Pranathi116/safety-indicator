import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Women Safety Indicator", layout="wide")

state_df = pd.read_csv("data/state_crime_summary.csv")
full_df = pd.read_csv("data/crime_data.csv")

state_df["State"] = state_df["State"].str.upper()
full_df["State"] = full_df["State"].str.upper()

city_to_state = {
    "HYDERABAD": "TELANGANA",
    "MUMBAI": "MAHARASHTRA",
    "PUNE": "MAHARASHTRA",
    "BANGALORE": "KARNATAKA",
    "CHENNAI": "TAMIL NADU",
    "DELHI": "DELHI",
    "KOLKATA": "WEST BENGAL",
    "AHMEDABAD": "GUJARAT",
    "JAIPUR": "RAJASTHAN",
    "LUCKNOW": "UTTAR PRADESH"
}

st.markdown("""
<h1>🚨 Women Safety Indicator</h1>
<p style='font-size:18px; color:gray;'>
AI-powered system to assess location safety for women in India
</p>
<hr>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 Enter Destination")
    place = st.text_input("Type a city or state name", placeholder="e.g., Hyderabad, Delhi, Kerala")
    analyze = st.button("🔮 Analyze Safety")

with col2:
    dot_color = "gray"
    safety_score = None

    if analyze and place:
        place_upper = place.upper()
        state = city_to_state.get(place_upper, place_upper)
        result = state_df[state_df["State"] == state]

        if not result.empty:
            row = result.iloc[0]
            risk = row["risk_level"]

           
            max_crime = state_df["total_crime"].max()
            safety_score = int(100 - (row["total_crime"] / max_crime) * 100)

            if risk == "High":
                dot_color = "red"
            elif risk == "Medium":
                dot_color = "orange"
            else:
                dot_color = "green"

    
    st.markdown(f"""
    <div style="display:flex; align-items:center;">
        <h3 style="margin-right:10px;">📊 Safety Report</h3>
        <div style="width:15px; height:15px; background-color:{dot_color};
                    border-radius:50%; margin-top:5px;"></div>
    </div>
    """, unsafe_allow_html=True)

    if analyze and place:
        place_upper = place.upper()
        state = city_to_state.get(place_upper, place_upper)
        result = state_df[state_df["State"] == state]

        if not result.empty:
            row = result.iloc[0]

            colA, colB, colC, colD = st.columns(4)
            colA.metric("Safety Score", f"{safety_score}/100")
            colB.metric("Risk Level", row["risk_level"])
            colC.metric("Total Crimes", int(row["total_crime"]))
            colD.metric("Rape Cases", int(row["Rape"]))

            st.markdown("#### 🔍 Crime Breakdown")
            st.write(row[['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']])

          
            past = full_df[(full_df["State"] == state) & (full_df["Year"] <= 2010)]
            recent = full_df[(full_df["State"] == state) & (full_df["Year"] >= 2018)]

            past_crime = past[['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']].sum().sum()
            recent_crime = recent[['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']].sum().sum()

            if past_crime > 0:
                trend_pct = int(((recent_crime - past_crime) / past_crime) * 100)
            else:
                trend_pct = 0

            st.markdown("#### 📈 Crime Trend")
            if trend_pct > 0:
                st.warning(f"Crime rate has increased by **{trend_pct}%** in recent years.")
            else:
                st.success(f"Crime rate has decreased by **{abs(trend_pct)}%** in recent years.")

            st.markdown("#### 🛡 Safety Tip")
            if row["risk_level"] == "High":
                st.error("High-risk area. Avoid late-night travel and stay in crowded, well-lit zones.")
            elif row["risk_level"] == "Medium":
                st.warning("Moderate risk. Prefer daytime travel and remain alert.")
            else:
                st.success("Relatively safe. Still follow basic safety precautions.")

        else:
            st.warning("❌ Location not found. Try a major city or full state name.")

    else:
        st.info("👈 Enter a place and click Analyze Safety")

st.markdown("<hr>", unsafe_allow_html=True)


st.markdown("## 🌍 India Safety Risk Map")

state_coords = {
    "ANDHRA PRADESH": [15.9129, 79.7400],
    "ARUNACHAL PRADESH": [28.2180, 94.7278],
    "ASSAM": [26.2006, 92.9376],
    "BIHAR": [25.0961, 85.3131],
    "CHHATTISGARH": [21.2787, 81.8661],
    "DELHI": [28.7041, 77.1025],
    "GOA": [15.2993, 74.1240],
    "GUJARAT": [22.2587, 71.1924],
    "HARYANA": [29.0588, 76.0856],
    "HIMACHAL PRADESH": [31.1048, 77.1734],
    "JHARKHAND": [23.6102, 85.2799],
    "KARNATAKA": [15.3173, 75.7139],
    "KERALA": [10.8505, 76.2711],
    "MADHYA PRADESH": [22.9734, 78.6569],
    "MAHARASHTRA": [19.7515, 75.7139],
    "MANIPUR": [24.6637, 93.9063],
    "MEGHALAYA": [25.4670, 91.3662],
    "MIZORAM": [23.1645, 92.9376],
    "NAGALAND": [26.1584, 94.5624],
    "ODISHA": [20.9517, 85.0985],
    "PUNJAB": [31.1471, 75.3412],
    "RAJASTHAN": [27.0238, 74.2179],
    "SIKKIM": [27.5330, 88.5122],
    "TAMIL NADU": [11.1271, 78.6569],
    "TELANGANA": [18.1124, 79.0193],
    "TRIPURA": [23.9408, 91.9882],
    "UTTAR PRADESH": [26.8467, 80.9462],
    "UTTARAKHAND": [30.0668, 79.0193],
    "WEST BENGAL": [22.9868, 87.8550]
}

m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

for _, row in state_df.iterrows():
    state = row["State"]
    if state in state_coords:
        lat, lon = state_coords[state]
        risk = row["risk_level"]

        color = "green"
        if risk == "High":
            color = "darkred"
        elif risk == "Medium":
            color = "orange"

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{state}<br>Total Crimes: {int(row['total_crime'])}<br>Risk: {risk}"
        ).add_to(m)

folium_static(m)
