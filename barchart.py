
import argparse
import json
import os
import pandas as pd
import requests
import matplotlib.pyplot as plt  # For visualization
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API key and URL for Yelp API
API_KEY = os.getenv("YELP_API_KEY")

# Define the endpoint and headers for authentication
url = "https://api.yelp.com/v3/businesses/search"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Define the parameters for your search
params = {
    "location": "Jersey City,NJ",  # Replace with the target city
    "categories": "blackowned, categories, resturants, shops", 
    "limit": 10,                   # Max results per request (Yelp caps this at 50)
    "sort_by": "rating"            # Other options: "rating", "review_count", "distance"
}

# Make the Yelp API request
response = requests.get(url, headers=headers, params=params)

# Check for successful response and load data into a DataFrame
if response.status_code == 200:
    data = response.json()
    yelp_businesses = data.get("businesses", [])

    # Convert Yelp data to a DataFrame
    yelp_df = pd.DataFrame(yelp_businesses)
    
    # Extract and clean necessary columns from Yelp data
    yelp_df = yelp_df[["name", "location", "rating", "phone", "categories"]]
    yelp_df["address"] = yelp_df["location"].apply(lambda x: x.get("address1", ""))
    yelp_df["city"] = yelp_df["location"].apply(lambda x: x.get("city", ""))
    yelp_df.drop(columns=["location"], inplace=True)

    # Extract category titles from nested category data
    yelp_df["categories"] = yelp_df["categories"].apply(lambda x: [cat["title"] for cat in x])

    # Flatten the list of categories and count each category
    all_categories = yelp_df["categories"].explode()  # Un-nest the category lists
    category_counts = all_categories.value_counts()   # Count occurrences of each category

    # Plot the category distribution as a bar chart
    plt.figure(figsize=(12, 8))
    category_counts.plot(kind="bar", color="orange")
    plt.title("Black Owned Businesses by Categories in Jersey City")
    plt.xlabel("Category")
    plt.ylabel("Number of Businesses")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Display the plot
    plt.show()

else:
    print(f"Error: {response.status_code} - {response.text}")
