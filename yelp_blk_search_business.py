import json
import pandas as pd
import os
import requests
import urllib.parse
import argparse

from dotenv import load_dotenv


load_dotenv()


# API key and URL for Yelp API
API_KEY = os.getenv("YELP_API_KEY")
YELP_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {
    "accept": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

def yelp_search_url(city: str, term: str = "Black owned") -> str:
    """
   Built a Yelp search URL using a city and term.
    Default term is set to 'Black owned'.
    """
    location_param = urllib.parse.quote_plus(city)
    term_param = urllib.parse.quote_plus(term)
    return f"{YELP_URL}?location={location_param}&term={term_param}"

def get_yelp_results(city: str) -> pd.DataFrame:
    """
    Fetch Yelp search results for Black-owned businesses in a specified city.
    """
    search_url = yelp_search_url(city)
    response = requests.get(search_url, headers=HEADERS)
    
    if response.status_code == 200:
        businesses = json.loads(response.text).get('businesses', [])
        print(f"Found {len(businesses)} Black-owned businesses in {city}.")
        return pd.DataFrame(businesses)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return pd.DataFrame()  # Return an empty DataFrame on error

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Retrieve Black-owned business data from Yelp")
    parser.add_argument('city', type=str, help="City and state in the format 'city, state_code'")
    args = parser.parse_args()

    city = args.city
    yelp_data = get_yelp_results(city)

    # Display the results


    if not yelp_data.empty:
        print(yelp_data[['name', 'location','categories']])
       
    else:
        print("No results showing")
