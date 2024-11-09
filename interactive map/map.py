import os
import pandas as pd
import requests
import folium  

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("YELP_API_KEY")
url = "https://api.yelp.com/v3/businesses/search"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

params = {
    "location": "Jersey City,NJ",           # Target city
    "term": "Black owned",                  # Term search for Black-owned businesses
    "categories": "blackowned",             # Category filter for Black-owned businesses
    "limit": 50,                            # Max results per request 
    "sort_by": "rating"                     # Sorting by rating
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    yelp_businesses = data.get("businesses", [])

   
    yelp_df = pd.DataFrame(yelp_businesses)
    
    # extract and clean necessary columns
    yelp_df["name"] = yelp_df["name"]
    yelp_df["rating"] = yelp_df["rating"]
    yelp_df["address"] = yelp_df["location"].apply(lambda x: x.get("address1", "N/A") if x else "N/A")
    yelp_df["city"] = yelp_df["location"].apply(lambda x: x.get("city", "N/A") if x else "N/A")

    # add latitude, longitude and image url
    yelp_df["latitude"] = yelp_df["coordinates"].apply(lambda x: x.get("latitude") if x else None)
    yelp_df["longitude"] = yelp_df["coordinates"].apply(lambda x: x.get("longitude") if x else None)
    yelp_df["image_url"] = yelp_df.get("image_url", None)

    # initialize a map centered on Jersey City
    m = folium.Map(location=[40.7282, -74.0776], zoom_start=13, tiles="CartoDB Positron")


    # markers for each business with images in the popup
    for index, row in yelp_df.iterrows():

# Choose color based on rating
        color = 'green' if row['rating'] > 4.9 else 'blue'
        

        # check if latitude and longitude are available
        if row["latitude"] and row["longitude"]:
            popup_text = f"""
            <b>{row['name']}</b><br>
            Rating: {row['rating']}<br>
            Address: {row['address']}<br>
            <img src="{row['image_url']}" width="150" height="150">
            """
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_text, max_width=300),
                # tooltip=row["name"]
                icon=folium.Icon(color=color)
            ).add_to(m)

    # save the map as an HTML file
    m.save("black_owned_businesses_map.html")
    print("Map has been saved as 'black_owned_businesses_map.html'")

else:
    print(f"Error: {response.status_code} - {response.text}")
