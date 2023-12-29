import streamlit as st

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Public": 0.035,  # kgCO2/km
        "Personal": 0.15,
        "Electricity": 0.82,  # kgCO2/kWh
        "Vegetarian": 0.55,  # kgCO2/meal, 2.5kgco2/kg
        "Vegan": 0.3,
        "Omnivoire": 1.25 ,
        "Waste": 0.5,  # kgCO2/kg
        "AverageEmissions": 1.68 #per capita, tons
    }
    ,"China": {
        "Public": 0.002,  # kgCO2/km
        "Personal": 0.16,
        "Electricity": 0.64,  # kgCO2/kWh
        "Vegetarian": 0.3,  # kgCO2/meal
        "Vegan": 0.4,
        "Omnivoire": 1.6,
        "Waste": 0.55,  # kgCO2/kg
        "AverageEmissions": 7.8 #per capita, tons
    }
    , "EU": {
        "Public": 0.002,  # kgCO2/km
        "Personal": 0.14,
        "Vegetarian": 0.35,  # kgCO2/meal,
        "Vegan": 0.32,
        "Omnivoire": 1.25,
        "Waste": 0.35,  # kgCO2/kg
        "AverageEmissions": 7.8 #per capita, tons
    }
    , "USA": {
        "Public": 0.002,  # kgCO2/km
        "Personal": 0.17,
        "Electricity": 0.48,  # kgCO2/kWh
        "Vegetarian": 0.45,  # kgCO2/meal, estimated by project drawdown
        "Vegan": 0.38,
        "Omnivoire": 1.54,
        "Waste": 0.45,  # kgCO2/kg
        "AverageEmissions": 13 #per capita, tons
    }
    , "Vietnam": {
        "Public": 0.002,  # kgCO2/km
        "Personal": 0.16,
        "Electricity": 0.6,  # kgCO2/kWh
        "Vegetarian": 0.33,  # kgCO2/meal, 2.5kgco2/kg
        "Vegan": 0.28,
        "Omnivoire": 1,
        "Waste": 0.45,  # kgCO2/kg
        "AverageEmissions": 3.7 #per capita, tons
    }
}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Calculate Your Carbon Footprint")

# Streamlit app code
st.title("Calculate Your Carbon Footprint")

# User inputs
st.subheader("Your Country")
country = st.selectbox("Select", ["China","EU","India","USA","Vietnam"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily commute distance (in km) 🚦")
    distance = st.number_input("Distance", 0, 100, key="distance_input")
    st.text("")
    st.text("")
    st.text("")
    
    st.subheader("Your diet information")
    meal_type = st.selectbox("Select your diet", ["Vegan","Vegetarian","Omnivoire"])

    st.subheader("Monthly electricity consumption (in kWh) ⚡")
    electricity = st.number_input("Electricity", 0, 1000, key="electricity_input")


with col2:
    st.subheader("Your mean of transportation")
    transportation = st.selectbox("Select your main mean of transportation", ["Public","Personal"])
    st.text("Personal transportation includes both car and motobike")

    st.subheader("Number of meals per day 🍲")
    meals = st.number_input("Meals", 0, 10, key="meals_input")   

    st.subheader("Waste generated per week (in kg) 🚮")
    waste = st.number_input("Waste", 0, 100, key="waste_input") 

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
#separate transportation_type
if transportation == "Personal": transportation_emissions = EMISSION_FACTORS[country]["Personal"] * distance
else: transportation_emissions = EMISSION_FACTORS[country]["Public"] * distance

electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity

#separate meal_type
if meal_type == "Vegan": diet_emissions = EMISSION_FACTORS[country]["Vegan"] * meals
elif meal_type == "Vegetarian": diet_emissions = EMISSION_FACTORS[country]["Vegetarian"] * meals
else: diet_emissions = EMISSION_FACTORS[country]["Omnivoire"] * meals

waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste
average_emissions = EMISSION_FACTORS[country]["AverageEmissions"]

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)
comparison = round((total_emissions/average_emissions)*100,2)

# Create a centered container for the button
if st.container():
    st.button("Calculate CO2 Emissions", key="calculate_button")
    st.markdown(
        """
        <style>
        #calculate_button {
            width: 200px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# if st.button("Calculate CO2 Emissions", key="calculate_button"):
    # Display results
    st.header("Results")
    
    st.subheader("Total Carbon Footprint")
    st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
    st.info(f"The average emissions per capita in your country is {average_emissions} tonnes in 2020. Your total carbon footprint is equivalent to {comparison}% {country}'s emissions per capita in 2020")

    st.subheader("Carbon Emissions by Category")
    st.info(f"🚦 Transportation: {transportation_emissions} tonnes CO2 per year")
    st.info(f"⚡ Electricity: {electricity_emissions} tonnes CO2 per year")
    st.info(f"🍲 Diet: {diet_emissions} tonnes CO2 per year")
    st.info(f"🚮 Waste: {waste_emissions} tonnes CO2 per year")


