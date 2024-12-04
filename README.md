# Documenation for yelp_blk_owned.py
This script retrieves data on Black-owned businesses from the Yelp API, BWDC, then extracts relevant fields and structures the data into a pandas DataFrame for easy analysis. The results include each business's name, rating, phone number, address, and city.


## Step 1: Data Collection
### 1.1 Yelp API Data Retrieval
- Used Yelp API to retrieve data about Black-owned businesses in New Jersey. 


### 1.2 Add Parameters 
- Create parameters for select city within black owned categories sorted by ratings. 

## Step 2: Data Extraction and Transformation
Retrieve the API response, load the data into a pandas DataFrame and extract the necessary fields.

1.Convert the JSON response to a DataFrame.
2. Select relevant columns (name, location, rating, phone).
3. Extract nested location fields (address1 and city).
4. Drop the nested location column after extraction.



## Sample Output
```
      name          rating   phone      address          city
0  Blended Flavors    4.5  +123456789  373 Columbus Ave  San Francisco
1     Taste & Co.    4.0  +987654321  456 Market St     San Francisco
```
