import streamlit as st

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 1.6,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal, 2.5kgco2/kg
        "Waste": 0.5,  # kgCO2/kg
        "AverageEmissions": 1.68 #per capita, tons
    }
    , "China": {
        "Transportation": 6.3,  # kgCO2/km
        "Electricity": 0.64,  # kgCO2/kWh
        "Diet": 1.6,  # kgCO2/meal
        "Waste": 0.55,  # kgCO2/kg
        "AverageEmissions": 7.8 #per capita, tons
    }
    , "EU": {
        "Transportation": 13.2,  # kgCO2/km
        "Electricity": 0.24,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal,
        "Waste": 0.35,  # kgCO2/kg
        "AverageEmissions": 7.8 #per capita, tons
    }
    , "USA": {
        "Transportation": 14.3,  # kgCO2/km
        "Electricity": 0.48,  # kgCO2/kWh
        "Diet": 1.54,  # kgCO2/meal, estimated by project drawdown
        "Waste": 0.45,  # kgCO2/kg
        "AverageEmissions": 13 #per capita, tons
    }
    , "Vietnam": {
        "Transportation": 1,  # kgCO2/km
        "Electricity": 0.6,  # kgCO2/kWh
        "Diet": 1,  # kgCO2/meal, 2.5kgco2/kg
        "Waste": 0.45,  # kgCO2/kg
        "AverageEmissions": 3.7 #per capita, tons
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Streamlit app code
st.title("Personal Carbon Calculator")

# User inputs
st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["China","EU","India","USA","Vietnam"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily commute distance (in km) 🚦")
    distance = st.number_input("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("Monthly electricity consumption (in kWh) ⚡")
    electricity = st.number_input("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("Waste generated per week (in kg) 🚮")
    waste = st.number_input("Waste", 0.0, 100.0, key="waste_input")

    st.subheader("Number of meals per day ")
    meals = st.number_input("Meals", 0, key="meals_input")

# Normalize inputs
if distance > 0:
    distance = distance * 365  # Convert daily distance to yearly
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly
if meals > 0:
    meals = meals * 365  # Convert daily meals to yearly
if waste > 0:
    waste = waste * 52  # Convert weekly waste to yearly

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste
average_emissions = EMISSION_FACTORS[country]["AverageEmissions"]

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)
average_emissions = round(average_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)
comparison = (total_emissions/average_emissions)*100

if st.button("Calculate CO2 Emissions"):

    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚦 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"⚡ Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍲 Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🚮 Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        st.warning(f"The average emissions per capita in your country is {average_emissions} tonnes in 2020. Your total carbon footprint is equivalent to {comparison}% of your emissions per capita in 2020")
