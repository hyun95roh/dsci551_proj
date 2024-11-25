"""
# Database Explorer

A utility script for exploring multiple databases with support for both MySQL and Firebase.

## User Instructions
To use this script, include these keywords in your input:
- "explore db": Required to activate database exploration
- "firebase": Optional - use Firebase (defaults to MySQL if not specified)
- "attribute": Optional - view table structure (defaults to showing rows if not specified)
- Table name: Required - specify either "CDC" or "FRED"

#EXAMPLE USAGE

explore db cdc                     # View CDC table data from MySQL
explore db firebase cdc           # View CDC table data from Firebase
explore db cdc attribute          # View CDC table structure from MySQL
explore db firebase fred         # View FRED table data from Firebase

"""

from pprint import pprint
from mysql import mysqlDB
from firebase import myfireDB
import json
import re 

def is_asking_sql_exploration(user_input) :
    user_input = user_input.lower() 
    pattern = r'\b(?:exploration|explore|describe|mysql|sql|db|database|schema|structure|design)\b'
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match: 
        print("You are looking to explore data...") 
        requested_dataset = what_dataset(user_input) 
        print(f"You are looking to explore: MySQL-- Dataset={requested_dataset} \n") 
        if requested_dataset: 
            ds = requested_dataset 
            if ds == 'CDC': 
                results = explore_sql_ds(user_input, ds) 
            elif ds == 'FRED': 
                results = explore_sql_ds(user_input, ds) 
            elif ds == 'STOCK': 
                results = explore_sql_ds(user_input, ds) 
            else: 
                results = "Unvalid dataset name. Valid names are : {CDC | FRED | STOCK } {attribute}"

        return True, results 
    
    else: 
        return False, "Invalid query for data exploration. Valid format: 'explore {CDC | FRED | STOCK}' or 'describe {CDC | FRED | STOCK}'"

def is_asking_fire_exploration(user_input) :
    user_input = user_input.lower() 
    pattern = r'\b(?:exploration|explore|describe|firebase|fire|db|database|schema|structure|design)\b'
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match: 
        print("You are looking to explore data...") 
        requested_dataset = what_dataset(user_input) 
        print(f"You are looking to explore database {requested_dataset} \n") 
        if requested_dataset: 
            ds = requested_dataset 
            if ds == 'CDC': 
                results = explore_fire_ds(user_input, ds) 
            elif ds == 'FRED': 
                results = explore_fire_ds(user_input, ds) 
            elif ds == 'STOCK': 
                results = explore_fire_ds(user_input, ds) 
            else: 
                results = "Unvalid dataset name. Valid names are : explore/describe {CDC | FRED | STOCK }"

        return True, results 
    
    else: 
        return False, "Invalid query for data exploration. Valid format: 'describe/explore {CDC | FRED | STOCK} attribute'"



def what_dataset(user_input):
    user_input = user_input.upper() #since all the names of dataset are uppercase.
    database_sets = {"CDC", "FRED","STOCK"}  
    selected_database = []

    for database in database_sets:
        if database in user_input:
            selected_database.append(database)

    return selected_database[0]

def is_attribute(user_input)-> bool:
    user_input = user_input.lower()
    if "attribute" in user_input:
        return True
    else:
        return False


def explore_sql_ds(user_input, which_dataset):
    try:
        explore = mysqlDB() #parameter
        explore.disconnect()
        explore.connect()
        # Get cursor and execute
        cursor = explore.connection.cursor()

        if is_attribute(user_input):
            cursor.execute(f"DESCRIBE {which_dataset}")
            results = cursor.fetchall()
            return results

        else:
            cursor.execute(f"SELECT * FROM {which_dataset} LIMIT 10;") #we might want to add more functions other then this
            results = cursor.fetchall()
            
            return results
    except Exception as e:
        print(f"Error accessing {which_dataset} database: {e}")
        return None
    finally:
        explore.disconnect()


def is_firebase(user_input):
    user_input = user_input.lower()

    if "firebase" in user_input:
        return True
    else:
        return False


def explore_fire_ds(user_input, which_dataset):
    try:
        explore = myfireDB()   

        if is_attribute(user_input): 
            bytes_data = explore.get(node= which_dataset)
            json_str = bytes_data.decode('utf-8')
            data = json.loads(json_str)
            
            # Get first record to examine its structure
            first_record = data[0]  # First item in the list
            
            # Get attributes from the first record
            attributes_info = {
                key: {
                    'type': str(type(first_record[key]))
                } for key in first_record.keys()
            }
            return attributes_info

        else:
            bytes_data = explore.get(node=which_dataset)
            # Convert bytes to string and parse JSON
            json_str = bytes_data.decode('utf-8')
            data = json.loads(json_str)
            # Now data is a list, get first 10
            return data[:5]

    except Exception as e:
        print(f"Error accessing CDC database: {e}")
        return None
    
