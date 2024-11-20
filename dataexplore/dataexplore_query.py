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

from database.mysql import mysqlDB
from database.firebase import myfireDB
import json


def is_asking_for_exploration(user_input) -> bool:
    #testing input
    # user_input = "example query for order by"

    user_input = user_input.lower()
    if "explore db" in user_input:
        print("You are looking to explore data...")

        requested_database = what_database(user_input)
        print(f"You are looking to explore database {requested_database} \n")
        if requested_database:
            db = requested_database
            if db == "cdc":
                if is_firebase:
                    results = explore_CDC_firebase(user_input)
                else: 
                    results = explore_CDC(user_input)
                print (results)
                
            elif db == "fred":
                if is_firebase:
                    results = explore_FRED_firebase(user_input)
                else: 
                    results = explore_FRED(user_input)
                print (results)

            elif db == "THIRD DB": #NEED TO ADD ANOTHER ONE
                results = explore_third()
                
            else:
                pass
        return True

    else:
        print("You are NOT looking to explore data")
        return



def what_database(user_input):
    user_input = user_input.lower()
    database_sets = {"cdc", "fred"} #need our third database!!!!!!
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


def explore_CDC(user_input):
    try:
        explore = mysqlDB() #parameter
        explore.disconnect()
        explore.connect()
        # Get cursor and execute
        cursor = explore.connection.cursor()

        if is_attribute(user_input):
            cursor.execute("DESCRIBE CDC")
            results = cursor.fetchall()
            return results

        else:
            cursor.execute("SELECT * FROM CDC LIMIT 10;") #we might want to add more functions other then this
            results = cursor.fetchall()
            
            return results
    except Exception as e:
        print(f"Error accessing CDC database: {e}")
        return None
    finally:
        explore.disconnect()

def explore_FRED(user_input):
    try:
        explore = mysqlDB() #parameter
        explore.disconnect()
        explore.connect()
        # Get cursor and execute
        cursor = explore.connection.cursor()

        if is_attribute(user_input):
            cursor.execute("DESCRIBE FRED")
            results = cursor.fetchall()
            return results

        else:
            cursor.execute("SELECT * FROM FRED LIMIT 10;") #we might want to add more functions other then this
            results = cursor.fetchall()
            
            return results
    except Exception as e:
        print(f"Error accessing FRED database: {e}")
        return None
    finally:
        explore.disconnect()


def explore_third():
    try:
        explore = mysqlDB() #parameter
        explore.disconnect()
        explore.connect()
        explore.execute("SELECT * FROM ___ LIMIT 10;")
        results = explore.fetchall()
        return results
    except Exception as e:
        print(f"Error accessing ___ database: {e}")
        return None
    finally:
        explore.disconnect()


def is_firebase(user_input):
    user_input = user_input.lower()

    if "firebase" in user_input:
        return True
    else:
        return False


def explore_CDC_firebase(user_input):
    try:
        explore = myfireDB()   

        if is_attribute(user_input): 
            bytes_data = explore.get(node="CDC")
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
            bytes_data = explore.get(node="CDC")
            # Convert bytes to string and parse JSON
            json_str = bytes_data.decode('utf-8')
            data = json.loads(json_str)
            # Now data is a list, get first 10
            return data[:5]

    except Exception as e:
        print(f"Error accessing CDC database: {e}")
        return None
    
# explore db firebase cdc


def explore_FRED_firebase(user_input):
    try:
        explore = myfireDB()   

        if is_attribute(user_input): 
            bytes_data = explore.get(node="FRED")
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
            bytes_data = explore.get(node="FRED")
            # Convert bytes to string and parse JSON
            json_str = bytes_data.decode('utf-8')
            data = json.loads(json_str)
            # Now data is a list, get first 10
            return data[:10]

    except Exception as e:
        print(f"Error accessing FRED database: {e}")
        return None