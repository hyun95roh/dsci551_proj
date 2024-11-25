from .mysql import mysqlDB  
from .firebase import myfireDB
import json
import pandas as pd  

def sql_retriever(response,print_out=None):
    retriever = mysqlDB() 
    retriever.disconnect()
    retriever.connect()
    #user_input = input("Do you want to see the retreival result? (y, n)")
    if print_out in ['y', 'yes', True]:
        # Execute the main query
        result = retriever.execute(response)  # Output: list of tuples

        # Dynamically handle column names based on the query
        try:
            # Extract result column names from the executed query
            column_names_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{response.split('FROM')[1].split()[0].strip()}'"
            table_columns = [col[0] for col in retriever.execute(column_names_query)]

            # Infer column names from the query structure if possible
            if "AVG(" in response or "SUM(" in response or "COUNT(" in response or "MAX(" in response or "MIN(" in response:
                # For aggregation queries, manually define result column names
                column_names = [col.strip() for col in response.split("SELECT")[1].split("FROM")[0].split(",")]
            else:
                column_names = table_columns  # Default to all table columns
        except IndexError:
            raise ValueError("Unable to determine column names for the query.")

        # Format the result as a table-like string
        rows = [f"{'  '.join(map(str, row))}" for row in result]
        formatted_result = f"{'  '.join(column_names)}\n" + "\n".join(rows)
        return formatted_result  # Return the formatted string

    else:
        return "You did not choose to print the actual data. Try again."

def fire_retriever(response, print_out=None): 
    if print_out in ['y', 'yes', True]:
        target_node = [i for i in ['CDC','FRED','STOCK'] if i in response][0]   
        base_url = 'https://dsci551-2f357-default-rtdb.firebaseio.com/'
        target_filter = None if response.find('?')==-1 else response[response.find('?')+1:] 
        print("---- target_node:",target_node)
        print("---- target_filter:",target_filter)

        retriever = myfireDB() 
        print("---- NOTE) We don't support DELETE and PUT to prevent data loss.") 
        
        #user_input_curl = input("Hit 'get', 'show', 'print' to see the retrieved data")
        user_input_curl = 'get' 
        user_input_curl = user_input_curl.lower() 
        command_list = ['get', 'show', 'print']

        while user_input_curl not in command_list:  
            print("Error. Available command: 'get', 'show','print' ")
            user_input_curl = input("Hit 'get', 'show', 'print' to see the retrieved data")  

        if user_input_curl in command_list:            
            output = retriever.get(node= target_node, filter= target_filter)
            print(output) 
            return output 


        elif user_input_curl in ['POST','PATCH']: 
            user_input1 = input("Choose one: FRED, STOCK, CDC") 
            if user_input1 == 'FRED':
                print('Input example: {"DATE":"01/31/2020", "Real Median Houshold Income in the US":99999} ')  
            elif user_input1 == 'STOCK': 
                print('Input example: {"DATE":"1987-03-31", "LLY": 10.99, "NVO": 5.4} ') 
            else: 
                print("""Input example: {"CLASSIFCATION": "Socioeconomic Characteristic" , "CLASSIFCATION_ID": 3,
                    "ESTIMATE": 30.0, "ESTIMATE_TYPE": "Percent of population, age adjusted", ESTIMATED_TYPE_ID: 1,
                    "GROUP":"Poverty level", "GROUP_ID":3 , "STANDARD_ERROR": 1.1, "SUBGROUP":"BELOW 100% FPL",
                    "SUBGROUP_ID":9, "SUBTOPIC":"Normal weight (BMI from 18.5 to 24.9)", "SUBTOPIC_ID":1,
                    "TIME_PERIOD":"1999-2002", "TIME_PERIOD": 2  
                    }""")

            user_input2 = input("Input your data ") 
            if user_input_curl == 'POST':
                return retriever.post(node=user_input1, data=user_input2) 
            if user_input_curl == 'PATCH':
                return retriever.patch(node=user_input1, data=user_input2) 
    
    else :
        return "You did not choose printing the actual data. Try again."


''' 
This design is for handling part_4, rather than part_2 and part_3.
-------------------------------------------------------------------
def fire_retriever(response): 
    retriever = myfireDB() 
    print("We don't support DELETE and PUT to prevent data loss.") 
    
    user_input_curl = input("[CURL] Choose one: GET / POST.")
    user_input_curl = user_input_curl.upper() 

    while user_input_curl not in ['GET', 'POST','PATCH']: 
        print("Error. Available command: 'GET' or 'POST' ")
        user_input_curl = input("[CURL] Choose one: GET / POST.")  

    if user_input_curl == 'GET':
        user_input1 = input("Choose one node: FRED, STOCK, CDC") 
        while user_input1 not in ['FRED','STOCK', 'CDC']:
            print("Error. Available node: FRED, STOCK, CDC")
            user_input1 = input("Choose one: FRED, STOCK, CDC") 
            
        user_input2 = input("[Optional] write your filter statement comming after 'json?'. For example: orderBy='$key'&equalTo='10'")
        user_input2 = user_input2.strip()  
        user_input2 = None if len(user_input2)==0 else user_input2 
        return retriever.get(node=user_input1,filter=user_input2) 


    elif user_input_curl in ['POST','PATCH']: 
        user_input1 = input("Choose one: FRED, STOCK, CDC") 
        if user_input1 == 'FRED':
            print('Input example: {"DATE":"01/31/2020", "Real Median Houshold Income in the US":99999} ')  
        elif user_input1 == 'STOCK': 
            print('Input example: {"DATE":"1987-03-31", "LLY": 10.99, "NVO": 5.4} ') 
        else: 
            print("""Input example: {"CLASSIFCATION": "Socioeconomic Characteristic" , "CLASSIFCATION_ID": 3,
                  "ESTIMATE": 30.0, "ESTIMATE_TYPE": "Percent of population, age adjusted", ESTIMATED_TYPE_ID: 1,
                  "GROUP":"Poverty level", "GROUP_ID":3 , "STANDARD_ERROR": 1.1, "SUBGROUP":"BELOW 100% FPL",
                  "SUBGROUP_ID":9, "SUBTOPIC":"Normal weight (BMI from 18.5 to 24.9)", "SUBTOPIC_ID":1,
                  "TIME_PERIOD":"1999-2002", "TIME_PERIOD": 2  
                  }""")

        user_input2 = input("Input your data ") 
        if user_input_curl == 'POST':
            return retriever.post(node=user_input1, data=user_input2) 
        if user_input_curl == 'PATCH':
            return retriever.patch(node=user_input1, data=user_input2) 
    
    else :
        return 
'''