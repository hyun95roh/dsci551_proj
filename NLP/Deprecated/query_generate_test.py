import requests
from typing import List, Dict, Any

#https://dsci551-2f357-default-rtdb.firebaseio.com/
DATABASE_URL = "https://hw1-48a40-default-rtdb.firebaseio.com/"

def generate_firebase_query(matched_attributes: List[str], time_period: str = None):
    # Map of attribute names to their corresponding field names in the database
    attribute_field_map = {
        "Normal weight (BMI from 18.5 to 24.9)": "SUBTOPIC",
        "Overweight or obese (BMI greater than or equal to 25.0)": "SUBTOPIC",
        "Obesity (BMI greater than or equal to 30.0)": "SUBTOPIC",
        "Grade 1 obesity (BMI from 30.0 to 34.9)": "SUBTOPIC",
        "Grade 2 obesity (BMI from 35.0 to 39.9)": "SUBTOPIC",
        "Grade 3 obesity (BMI greater than or equal to 40.0)": "SUBTOPIC",
        "Below 100% FPL": "SUBGROUP",
        "100%-199% FPL": "SUBGROUP",
        "200%-399% FPL": "SUBGROUP",
        "400% or more FPL": "SUBGROUP"
    }
    
    # Construct the query parameters
    query_params = {}
    for attr in matched_attributes:
        if attr in attribute_field_map:
            field = attribute_field_map[attr]
            query_params[f'orderBy="{field}"'] = f'equalTo="{attr}"'
    
    if time_period:
        query_params['orderBy="TIME_PERIOD"'] = f'equalTo="{time_period}"'
    
    # Construct the URL
    url = f"{DATABASE_URL}csv.json"
    if query_params:
        url += "?" + "&".join([f"{k}&{v}" for k, v in query_params.items()])
    
    return url

def execute_query(url: str) -> List[Dict[str, Any]]:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [item for item in data.values() if item is not None]
    else:
        print(f"Error: {response.status_code}")
        return []

# Example usage:
matched_attrs = ["Obesity (BMI greater than or equal to 30.0)", "Below 100% FPL"]
query_url = generate_firebase_query(matched_attrs, time_period="2015-2018")
print("Generated query URL:", query_url)

results = execute_query(query_url)
for item in results:
    print(item)