# 🌍 Global Energy Dashboard

An interactive data visualization dashboard built with **Streamlit**, **Pandas**, and **Plotly** to explore global energy consumption trends by country and source.

---

## Features

* **Multi-country selection** and **year range slider**
* Interactive **line charts** for:

  * Total primary energy consumption
  * Solar, wind, coal, gas, nuclear, hydro energy
  * Per capita energy consumption
* **Pie chart** showing the energy structure of a selected country
* **World map (choropleth)** of energy consumption per country
* **Analysis** of the share of solar and wind in total energy use

---

## Demo

You can try the live version on [Streamlit Cloud](https://energy-dashboard-dijunasvmxhqthymfn2ul7.streamlit.app/) 

---

## Installation

```bash
# Clone the repository
git clone https://github.com/alina-bobrova/energy-dashboard.git
cd energy-dashboard

# Create virtual environment
python -m venv venv
Mac: source venv/bin/activate  
Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run energy_dashboard.py
```

---

## File Structure

```
energy-dashboard/
├── energy_dashboard.py       # Main Streamlit app
├── requirements.txt          # Dependencies
└── README.md                 # Project description
```

---

## requirements.txt

```
streamlit
pandas
plotly
```

---

## Data Source

Data is provided by [Our World in Data - Energy Dataset](https://github.com/owid/energy-data)

