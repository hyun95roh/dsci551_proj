from mysql import mysqlDB  
from firebase import myfireDB
import json 

def sql_retriever(response):
    retriever = mysqlDB() 
    retriever.disconnect()
    retriever.connect()
    user_input = input("Do you want to see the retreival result? (y, n)")
    if user_input.lower() in ['y','yes']:
        return retriever.execute(response)
    else: 
        return 

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