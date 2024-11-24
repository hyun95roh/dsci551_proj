from attribute_matcher import match_attributes
from attribute_sets import attribute_sets
from example_query import is_asking_sql_example, is_asking_fire_example 
from mysql import mysqlDB  
from firebase import myfireDB 
from retreive_data import sql_retriever, fire_retriever


def handle_user_input(user_first_nlq, user_input_DB=None, user_query=None, print_out=None):
    """
    Handles the user input based on their intent.

    Args:
        user_input_nlq (str): User's intent (examples, database, or NLQ).
        user_input_DB (str, optional): Database choice (MySQL or Firebase). Defaults to None.
        user_query (str, optional): The actual query entered by the user. Defaults to None.

    Returns:
        str: The response to be displayed or processed further.
    """
    user_input_nlq = user_first_nlq.lower()

#    if user_input_nlq in ['1', 'db', 'database']:
#        if not user_input_DB:
#            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"
#        if not user_query:
#            return "Enter your query (or type 'quit' to exit):"
#        else:
#            return "Invalid database choice. Please choose either MySQL or Firebase."


    if user_input_nlq in ['2', 'examples', 'example']:
        if not user_input_DB:
            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"
        
        if user_input_DB in ['1', 'sql', 'mysql']:
            boolean, response = is_asking_sql_example(user_query)
            if boolean: 
                if print_out in ['y','yes',True]: # Print out the actual data
                    return response, sql_retriever(response, print_out)
                
                return response # Skip print out the actual data  
            else:
                return "Your input does not match an example SQL query. Please refer to available commands: example query {where|groupby|orderby|having|aggregation}."
        
        elif user_input_DB in ['2', 'firebase']:
            boolean, response = is_asking_fire_example(user_query)
            if boolean:
                if print_out in ['y','yes',True]: 
                    return response, fire_retriever(response, print_out)
                return response 
            else:
                return "Your input does not match an example Firebase query. Please refer to available commands: example query GET."
        
        else:
            return "Invalid database choice. Please choose either MySQL or Firebase."


#    if user_input_nlq in ['3', 'nlq']:
#        if not user_input_DB:
#            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"
#        if not user_query:
#            return "Enter your query (or type 'quit' to exit):"
#        else:
#            return "Invalid database choice. Please choose either MySQL or Firebase."

    return "Invalid input. Please choose one of the available options: 1 (examples), 2 (database), or 3 (NLQ)."


def main():
    while True:
        print("Hello! How can I help you?") 
        user_input_nlq = input("Please Input your natural language query, or choose a number from example natural language query(NLQ)---> Example NLQ: 1)I want to see query examples, 2)Tell me about database, 3)I'll input NLQ")
        user_input_nlq = user_input_nlq.lower() 
        while user_input_nlq not in ['1','2','3','quit','examples','example','nlq','natural language','explore','database','db']:
            print("Error: Available inputs are: 1 or 2")
            user_input_nlq = input("Your query should keywords,i.e., {example(s)|nlq|explore database|db}. --> Query format e.g.: I want to see query examples, I'll input NLQ")
            continue 
        if user_input_nlq == 'quit': 
            break 
        
        if user_input_nlq in ['2','examples','example']:
            user_input_DB = input("Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase")
            user_input_DB = user_input_DB.lower() 
            while user_input_DB not in ['1','2','mysql','sql','firebase','fire'] :
                print("Sorry. Please refer to available commands: { 1 | 2 | mysql | sql | firebase | fire } ") 
                user_input_DB = input("Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase")
                continue 

            if user_input.lower() == 'quit':
                break

            if user_input_DB in ['1','sql','mysql']:  #when user pick DB=SQL
                user_input = input("Sorry. Please refer to available commands: example query {where|groupby|orderby|having|aggregation} (or 'quit' to exit)")
                print(f"Your Input: {user_input}")
                # is_asking_for_example(user_input) #outputs bool. user should start with "example query" to access
                boolean, response = is_asking_sql_example(user_input)  
                
                if boolean :
                    #print("Response:", response)
                    sql_retriever(response)   
                    continue 
                else:
                    print("run rest of code")
                    continue
                # match_sentence()

            else: #when user pick DB=Firebase 
                user_input = input("Sorry. Please refer to available commands: example query GET (or 'quit' to exit)")
                boolean, response = is_asking_fire_example(user_input)
                if boolean :
                    fire_retriever(response) 
                    continue  
                else: 
                    print("run rest of code") 
                    continue 

        if user_input_nlq in ['3','nlq']: # This handles NLQ to DB query.
            user_input_DB = input("Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase")
            user_input_DB = user_input_DB.lower() 
            while user_input_DB not in ['1','2','sql','mysql','firebase','fire'] :
                print("Error: Available inputs are: 1 or 2") 
                user_input_DB = input("Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase")
                continue 

            user_input = input("Enter your query (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break

            if user_input_DB==['1','sql','mysql']:  #when user pick DB=SQL
                print(f"Your Input: {user_input}")
                # is_asking_for_example(user_input) #outputs bool. user should start with "example query" to access
                # boolean, response = *** Place NLQ-parser here *** 

            else :  # when user pick DB=Firebase
                print(f"Your Input: {user_input}")
                # is_asking_for_example(user_input) #outputs bool. user should start with "example query" to access
                # boolean, response = *** Place NLQ-parser here *** 
            pass

if __name__ == "__main__":
    main()

#####################################################################################
#### DEPRECATED Functions ###########################################################
'''
def match_sentence():
    sentence = "normal weight. unemployment. What is the average of Real Median Household Income when the population percentage below 100 percentage FPL exceeds 30"

    matched_sets = match_attributes(sentence, attribute_sets)

    if matched_sets:
        print("Matched attributes:")
        for set_name, attributes in matched_sets.items():
            print(f"  {set_name}: {attributes}")
    else:
        print("No matches found in any set.")

# # If you want to know which specific sets had matches
# matched_set_names = list(matched_sets.keys())
# print(f"\nSets with matches: {matched_set_names}")

#NEXT: turn "matched attribtues" into query.
'''