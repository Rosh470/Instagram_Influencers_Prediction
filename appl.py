import streamlit as st
import pickle
import pandas as pd

# Load the dataset containing influencers data
df = pd.read_excel("instagram_inluencers.xlsx")

# Get unique values for country, Category 1, and Category 2
unique_countries = df["country"].unique().tolist()
unique_categories = set(
    df["Category_1"].unique().tolist() + df["Category_2"].unique().tolist()
)
unique_categories.discard("nan")  # Remove 'nan' value

# Streamlit UI
st.title("Influencer Potential Reach Predictor")

# Select country
country = st.selectbox("Select Country:", unique_countries)

# Select categories
selected_categories = st.multiselect("Select Categories:", list(unique_categories))


# Function to predict potential reach
def predict_potential_reach(country, categories):
    # Filter the dataset based on selected country and categories
    filtered_df = df[df["country"] == country]
    for category in categories:
        filtered_df = filtered_df[filtered_df["Categories"].str.contains(category)]

    # Load the trained Linear Regression model
    with open("linear_regression_model.pkl", "rb") as file:
        model = pickle.load(file)

    # Predict potential reach using the trained model
    X = filtered_df[["followers", "Authentic_Engagement", "Average_Engagement"]]
    filtered_df["Estimated_Reach"] = model.predict(X)

    # Sort by estimated reach and select top 10 influencers
    top_influencers = filtered_df.sort_values(
        by="Estimated_Reach", ascending=False
    ).head(10)

    return top_influencers[["instagram name", "followers", "Estimated_Reach"]]


# Predict potential reach and display results
if st.button("Predict Potential Reach"):
    st.subheader("Top 10 Influencers")
    top_influencers = predict_potential_reach(country, selected_categories)
    st.write(top_influencers)
