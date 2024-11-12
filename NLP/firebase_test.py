import requests
import json

DATABASE_URL = "https://dsci551-2f357-default-rtdb.firebaseio.com/"
response = requests.get(f"{DATABASE_URL}/CDC.json")

if response.status_code == 200:
    cdc_data = response.json()
    
    # Initialize an empty list to store the filtered data
    filtered_data = []
    
    # Iterate through each item in the CDC data
    for item in cdc_data:
        # Check if the SUBTOPIC_ID is 1
        if item['SUBTOPIC_ID'] == 1:
            # If it is, add the ESTIMATE_TYPE_ID to our filtered list
            filtered_data.append(item['ESTIMATE_TYPE_ID'])



    print(f"Found {len(filtered_data)} ESTIMATE_TYPE_ID values where SUBTOPIC_ID == 1:")
    print(filtered_data)

else:
    print(f"Error fetching data: {response.status_code}")




# ################################################################################################
# def get_database_structure():
#     # Make a GET request to the root of the database
#     response = requests.get(f"{DATABASE_URL}.json")
    
#     if response.status_code == 200:
#         # If the request is successful, return the JSON data
#         return response.json()
#     else:
#         # If there's an error, print the status code and return None
#         print(f"Error: {response.status_code}")
#         return None

# def print_structure(data, indent=0):
#     # Recursively print the structure of the data
#     if isinstance(data, dict):
#         for key, value in data.items():
#             print("  " * indent + str(key))
#             print_structure(value, indent + 1)
#     elif isinstance(data, list):
#         print("  " * indent + f"(Array with {len(data)} items)")
#         if len(data) > 0:
#             print_structure(data[0], indent + 1)
#     else:
#         print("  " * indent + f"({type(data).__name__})")

# # Get the database structure
# structure = get_database_structure()

# if structure:
#     print("Database Structure:")
#     print_structure(structure)
# else:
#     print("Failed to retrieve database structure.")

# # Optionally, you can also save the full structure to a JSON file
# with open('database_structure.json', 'w') as f:
#     json.dump(structure, f, indent=2)
#     print("\nFull structure saved to 'database_structure.json'")