import streamlit as st
import pandas as pd
import joblib
import os
import json
import threading

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "diabetes_model.pkl")
model = joblib.load(model_path)

# Load translations from the JSON file
with open("translations.json", "r") as file:
    translations = json.load(file)

# Ensure Hindi is at the top of the available languages list
available_languages = ["English"] + [lang for lang in translations.keys() if lang != "English"]
# BMI Visualization (simple gauge bar using st.progress or st.markdown)
bmi_percent = min(int((bmi_value / 40) * 100), 100)
right_col.markdown("#### BMI Level")
right_col.progress(bmi_percent)

# Pie Chart: Health Conditions (yes/no converted to pie chart)
health_fields = ["HighBP", "HighChol", "Smoker", "Stroke", "HeartDiseaseorAttack", 
                 "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "DiffWalk"]

health_data = {
    "Condition": [],
    "Status": []
}
for field in health_fields:
    health_data["Condition"].append(current_translations.get(field, field))
    health_data["Status"].append("Yes" if input_df[field].iloc[0] == 1 else "No")

pie_df = pd.DataFrame(health_data)

# Show Pie Chart
right_col.markdown("#### Health Conditions Overview")
fig_pie = px.pie(pie_df, names="Condition", color="Status",
                 title="Health Factors (Yes vs No)", hole=0.4)
right_col.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart: Health Ratings
rating_df = pd.DataFrame({
    "Category": [
        current_translations["general_health"],
        current_translations["mental_health"],
        current_translations["physical_health"]
    ],
    "Value": [
        input_df["GenHlth"].iloc[0],
        input_df["MentHlth"].iloc[0],
        input_df["PhysHlth"].iloc[0]
    ]
})

right_col.markdown("#### Health Ratings Breakdown")
fig_bar = px.bar(rating_df, x="Category", y="Value", color="Category",
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title="User Health Ratings")
right_col.plotly_chart(fig_bar, use_container_width=True)
