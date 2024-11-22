"""
# SQL Query Handler

A utility script for processing SQL queries with support for MySQL and Firebase databases.

## User Input Format
The input MUST start with 'sql' followed by a space, then your SQL query:
sql [YOUR_QUERY]

## Example Usage

sql SELECT * FROM table_name
sql SHOW TABLES
sql DESCRIBE my_table

## Note
This is a preprocessing script for SQL queries. 
The actual execution of queries should be handled by appropriate database functions.
"""


from database.mysql import mysqlDB
from nlq_to_sql import NLQtoSQLConverter
import json

def is_sql_query(user_input) -> bool:

    # user_input = user_input.lower()
    if user_input.startswith("sql "):
        print("You are looking to input mysql query...")
        user_input = user_input[4:]
        print(f"\nYour user input is: {user_input}")

        converter = NLQtoSQLConverter()
        sql_query = converter.convert_nlq_to_sql(user_input)
        sql_query = sql_query + ";"
        print("\nYour query is: ", sql_query)

        results = explore_mysql(sql_query)
        print(results)

        return sql_query
    return False


def explore_mysql(query):
    try:
        explore = mysqlDB() #parameter
        explore.disconnect()
        explore.connect()
        # Get cursor and execute
        cursor = explore.connection.cursor()

        cursor.execute(query)
        results = cursor.fetchall()
            
        return results
    except Exception as e:
        print(f"Error accessing database: {e}")
        return None
    finally:
        explore.disconnect()