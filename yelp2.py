import json
import pandas as pd
import os
import requests
import urllib.parse
import argparse
import folium  # Library for map visualization
from dotenv import load_dotenv

# Load environment variables
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
    Build a Yelp search URL using a city and term.
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
        
        # Flatten data and include latitude and longitude for map visualization
        business_data = []
        for biz in businesses:
            business_data.append({
                "name": biz.get("name"),
                "rating": biz.get("rating"),
                "latitude": biz["coordinates"].get("latitude"),
                "longitude": biz["coordinates"].get("longitude"),
                "address": biz["location"].get("address1"),
                "city": biz["location"].get("city"),
                "categories": [cat["title"] for cat in biz.get("categories", [])]
            })
        
        return pd.DataFrame(business_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def create_interactive_map(df: pd.DataFrame, city: str) -> None:
    """
    Generate and save an interactive map of businesses using folium.
    """
    # Center the map around the average location of businesses
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=13, tiles="CartoDB Positron")
    
    # Add markers to the map
    for _, row in df.iterrows():
        # Choose color based on rating
        color = 'green' if row['rating'] >= 4 else 'blue'
        popup_text = f"{row['name']} - Rating: {row['rating']}<br>Address: {row['address']}<br>Category: {', '.join(row['categories'])}"
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    # Save the map as an HTML file
    map_file = f"{city.replace(', ', '_')}_black_owned_businesses_map2.html"
    m.save(map_file)
    print(f"Map saved as {map_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Retrieve Black-owned business data from Yelp")
    parser.add_argument('city', type=str, help="City and state in the format 'city, state_code'")
    args = parser.parse_args()

    city = args.city
    yelp_data = get_yelp_results(city)

    if not yelp_data.empty:
        print(yelp_data[['name', 'address', 'categories']])
        
        # Generate and save the interactive map
        create_interactive_map(yelp_data, city)
    else:
        print("No results found")
