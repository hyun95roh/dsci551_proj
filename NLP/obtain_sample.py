from mysql import mysqlDB  
from firebase import myfireDB

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
    if user_input_curl not in ['GET', 'POST']: 
        print("Error. Available command: 'GET' or 'POST' ")
    user_input_node = input("Choose one: FRED, STOCK, CDC") 
    user_input_filter = input("Type your filter query. For skip, just press enter.") 

    if user_input_curl == 'GET':
        user_input1 = input("Do you want to see the retreival result? (y, n)")
        if user_input1.lower() in ['y','yes']: 
            return retriever.get(node=user_input_node, filter=user_input_filter) 
        else:
            return 

    else :
        user_input