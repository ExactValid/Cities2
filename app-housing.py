
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Title
st.title("California Housing Data (1990) by 瞿佳沐")

# Load dataset
df = pd.read_csv(Path(__file__).parent / "housing.csv")

# 2. Slider: minimum median house value
house_value_filter = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)

# 3. Subheader
st.subheader("See more filters in the sidebar:")

# 4. Sidebar multiselect: ocean proximity
location_types = df["ocean_proximity"].dropna().unique().tolist()

location_filter = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

# 5. Sidebar radio: median income
income_filter = st.sidebar.radio(
    "Choose income level",
    ["Low", "Medium", "High"]
)

# Filter by median house value
df = df[df["median_house_value"] >= house_value_filter]

# Filter by ocean proximity
df = df[df["ocean_proximity"].isin(location_filter)]

# Filter by income level
if income_filter == "Low":
    df = df[df["median_income"] <= 2.5]

elif income_filter == "Medium":
    df = df[
        (df["median_income"] > 2.5) &
        (df["median_income"] < 4.5)
    ]

elif income_filter == "High":
    df = df[df["median_income"] >= 4.5]

# 6. Display map
st.subheader("California Housing Map")

if not df.empty:
    st.map(df)

    # 7. Histogram with 30 bins
    st.subheader("Median House Value Distribution")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        df["median_house_value"].dropna(),
        bins=30,
        edgecolor="black"
    )

    ax.set_xlabel("Median House Value ($)")
    ax.set_ylabel("Number of Districts")
    ax.set_title("Distribution of Median House Values")

    st.pyplot(fig)
    plt.close(fig)

else:
    st.warning("No districts match the selected filters.")
