from attribute_matcher import match_attributes
from attribute_sets import attribute_sets
from example_query import is_asking_for_example
from mysql import mysqlDB  
from firebase import myfireDB 
from obtain_sample import sql_retriever, fire_retriever

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


def main():
    while True:
        user_input_DB = input("Which DB do you want? Input the number: 1. MySQL / 2.Firebase")
        if user_input_DB not in ['1','2'] :
            print("Error: Available inputs are: 1 or 2") 
            continue 

        user_input = input("Enter your query (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        print(f"Your Input: {user_input}")
        # is_asking_for_example(user_input) #outputs bool. user should start with "example query" to access
        boolean, response = is_asking_for_example(user_input) 
         
        if boolean and user_input_DB=='1':
            #print("Response:", response)
            sql_retriever(response)   
            continue 
        elif boolean and user_input_DB=='2':
            fire_retriever(response)
            continue 
        else:
            print("run rest of code")
            continue
        # match_sentence() 
        


if __name__ == "__main__":
    main()