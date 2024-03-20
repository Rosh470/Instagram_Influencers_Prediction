import streamlit as st
import pickle
import pandas as pd

# Load the trained Linear Regression model
with open("linear_regression_model.pkl", "rb") as file:
    model = pickle.load(file)


# Function to predict potential reach
def predict_potential_reach(country, categories):
    # Load the dataset containing influencers data
    df = pd.read_excel(
        "combined_data.xlsx"
    )  # Replace 'influencers_data.csv' with your dataset file name

    # Filter the dataset based on selected country and categories
    filtered_df = df[df["country"] == country]
    for category in categories:
        filtered_df = filtered_df[filtered_df["Categories"].str.contains(category)]

    # Predict potential reach using the trained model
    X = filtered_df[["followers", "Authentic_Engagement", "Average_Engagement"]]
    filtered_df["Estimated_Reach"] = model.predict(X)

    # Sort by estimated reach and select top 10 influencers
    top_influencers = filtered_df.sort_values(
        by="Estimated_Reach", ascending=False
    ).head(10)

    return top_influencers[["instagram name", "Estimated_Reach"]]


# Streamlit UI
st.title("Influencer Potential Reach Predictor")

# Select country
country = st.selectbox(
    "Select Country:",
    [
        "Argentina",
        "India",
        "Brazil",
        "United States",
        "France",
        "South Korea",
        "Indonesia",
        "Mexico",
        "Ethiopia",
        "Spain",
        "Turkey",
        "Italy",
        "Morocco",
        "Poland",
        "China",
        "United Kingdom",
        "Iran",
        "Russia",
        "Colombia",
        "Australia",
        "Philippines",
        "Yemen",
        "Egypt",
        "United Arab Emirates",
        "Germany",
        "Thailand",
        "Portugal",
        "Nigeria",
        "Iraq",
        "Japan",
        "Algeria",
        "Albania",
        "Syria",
        "Chile",
        "Other",
    ],
)  # Add your country list here

# Select categories
categories = st.multiselect(
    "Select Categories:",
    [
        "Humor & Fun & Happiness",
        "Modeling",
        "Winter sports",
        "Gaming",
        "Machinery & Technologies",
        "NFT",
        "Family",
        "Water sports",
        "Cars & Motorbikes",
        "Travel",
        "Shows",
        "Fashion",
        "Nature & landscapes",
        "Animals",
        "Food & Cooking",
        "Cinema & Actors/actresses",
        "Science",
        "Literature & Journalism",
        "Racing Sports",
        "Business & Careers",
        "Music",
        "Education",
        "Photography",
        "Luxury",
        "Fitness & Gym",
        "Comics & sketches",
        "Finance & Economics",
        "Lifestyle",
        "Art/Artists",
        "Clothing & Outfits",
        "Shopping & Retail",
        "Trainers & Coaches",
        "Kids & Toys",
        "Politics",
        "Beauty",
        "Management & Marketing",
        "Sports with a ball",
        "Adult content",
        "Computers & Gadgets",
    ],
)  # Add your category list here

# Predict potential reach and display results
if st.button("Predict Potential Reach"):
    st.subheader("Top 10 Influencers")
    top_influencers = predict_potential_reach(country, categories)
    st.write(top_influencers)
