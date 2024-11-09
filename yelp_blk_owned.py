import argparse
import json
import os
import pandas as pd
import requests


from dotenv import load_dotenv


load_dotenv()


# API key and URL for Yelp API
API_KEY = os.getenv("YELP_API_KEY")

# define the endpoint and headers for authentication
url = "https://api.yelp.com/v3/businesses/search"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# define the parameters for your search
params = {
    "location": "Jersey City,NJ",  # Target city
    "term": "Black owned",         # Term search for Black-owned businesses
    "categories": "blackowned",    
    "limit": 50,
    "sort_by": "rating"            
}

# make the Yelp API request
response = requests.get(url, headers=headers, params=params)

# check for successful response and load data into a DataFrame
if response.status_code == 200:
    data = response.json()
    yelp_businesses = data.get("businesses", [])


    
    # convert Yelp data to a DataFrame
    yelp_df = pd.DataFrame(yelp_businesses)
    
    # extract and clean necessary columns from Yelp data
    yelp_df = yelp_df[["name", "rating", "display_phone","location",]]
    yelp_df["address"] = yelp_df["location"].apply(lambda x: x.get("address1", ""))
    yelp_df["city"] = yelp_df["location"].apply(lambda x: x.get("city", ""))
    

    print(yelp_df)
else:
    print(f"Error: {response.status_code} - {response.text}")
