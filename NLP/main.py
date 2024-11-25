from .script.example_query import is_asking_sql_example, is_asking_fire_example 
from .script.dataexplore_query import is_asking_sql_exploration, is_asking_fire_exploration
from .script.retreive_data import sql_retriever, fire_retriever
from .NLQ_implementation.nlq_to_fbquery import NLQtoFBConverter
from .NLQ_implementation.nlq_to_sql import NLQtoSQLConverter

# handle_user_input is a gateway function between Streamlit and Demo(for db exploration, example query, data retrieval)
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
    user_input_nlq = user_first_nlq.lower() #-- NLQ at the first stage(initial)

    ###############################################################################
    # GATE 1 : DB Exploration #####################################################
    if user_input_nlq in ['1', 'db', 'database']:
        if not user_input_DB:
            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"

        if user_input_DB in ['1', 'sql', 'mysql'] :
            boolean, response = is_asking_sql_exploration(user_query)
            if boolean: 
                if print_out in ['y','yes',True]: 
                    return "Here is a snapshot of your interest:", response 
                return response, None 
            else: 
                return "Please refer to available commands: {}", None  
        elif user_input_DB in ['2','firebase'] : 
            boolean, response = is_asking_fire_exploration(user_query) 
            if boolean: 
                if print_out in ['y','yes',True]: #print out the exploration result 
                   return "Here is a snapshot of your interest:", response 
                return response, None # Skip print out the actual data 
        else:
            return "Invalid database choice. Please choose either MySQL or Firebase.", None 

    ###############################################################################
    # GATE 2 : Example queries ####################################################
    if user_input_nlq in ['2', 'examples', 'example']:
        if not user_input_DB:
            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"
        
        if user_input_DB in ['1', 'sql', 'mysql']:
            boolean, response = is_asking_sql_example(user_query) #user_query means 'specific' query example or request.
            if boolean: 
                if print_out in ['y','yes',True]: # Print out the actual data
                    return response, sql_retriever(response, print_out)
                
                return response, None # Skip print out the actual data  
            else:
                return "Your input does not match an example SQL query. Please refer to available commands: example query {where|groupby|orderby|having|aggregation}.", None 
        
        elif user_input_DB in ['2', 'firebase']:
            boolean, response = is_asking_fire_example(user_query)
            if boolean:
                if print_out in ['y','yes',True]: 
                    return response, fire_retriever(response, print_out)
                return response, None  
            else:
                return "Your input does not match an example Firebase query. Please refer to available commands: example query GET.", None
        
        else:
            return "Invalid database choice. Please choose either MySQL or Firebase.", None 

        # GATE 3 : Free NLQ handling  #################################################
    if user_input_nlq in ['3', 'nlq']:
        if not user_input_DB:
            return "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"
        
        if user_input_DB in ['1', 'sql', 'mysql']:
            boolean = True 
            #example query = "Show top 5 income values from FRED"
            sql_converter = NLQtoSQLConverter()
            response = sql_converter.convert_nlq_to_sql(user_query) #user_query means 'specific' query example or request.
            
            if boolean: 
                if print_out in ['y','yes',True]: # Print out the actual data
                    return response, sql_retriever(response, print_out)
                
                return response, None # Skip print out the actual data  
            else:
                return "Your input does not match an example SQL query. Please refer to available commands: example query {where|groupby|orderby|having|aggregation}.", None 
        
        elif user_input_DB in ['2', 'firebase']:
            boolean = True 
            #example query = "Show last 10 income values from FRED start from 2024-01-01 end to 2024-02-03"

            fb_converter = NLQtoFBConverter()
            response = fb_converter.output_query(user_query) #user_query means 'specific' query example or request.
            
            response = "curl 'https://dsci551-2f357-default-rtdb.firebaseio.com/FRED.json'"
            if boolean:
                if print_out in ['y','yes',True]: 
                    return response, fire_retriever(response, print_out)
                return response, None  
            else:
                return "Your input does not match an example Firebase query. Please refer to available commands: example query GET.", None
        
        else:
            return "Invalid database choice. Please choose either MySQL or Firebase.", None 


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