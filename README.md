 Women Safety Indicator

Project Overview

An interactive data-driven web application that analyzes historical crime data to assess the safety risk level of Indian cities and states for women. The system computes a safety score, classifies regions into risk categories using rule-based logic, and visualizes the results on an interactive India map through a Streamlit-based interface.

---

Features

* City/State-based safety analysis
* Category-wise crime statistics
* Safety score generation (0–100 scale)
* Risk level classification (High / Moderate / Low)
* Interactive India map with color-coded safety markers
* Real-time results through a web-based UI

---

Tech Stack

* **Python** – Core programming language
* **pandas** – Dataset loading, cleaning, and processing
* **Streamlit** – Interactive web application framework and local deployment
* **Folium** – Interactive map visualization using OpenStreetMap

---

 How to Run the Project

1. Clone the Repository

```bash
git clone https://github.com/your-username/women-safety-indicator.git
cd women-safety-indicator
```

2. Install Dependencies

```bash
pip install pandas streamlit folium streamlit-folium
```

3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```
