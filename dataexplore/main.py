from attribute_matcher import match_attributes
from attribute_sets import attribute_sets
from example_query import is_asking_for_example
from dsci551_proj.NLP.dataexplore_query import is_asking_for_exploration
# from database.firebase import myfireDB
# from database.mysql import mysqlDB

def match_sentence(): #not currently in use
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
        user_input = input("Enter your query (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        print(f"Your Input: {user_input}")
        # is_asking_for_example(user_input) #outputs bool. user should start with "example query" to access
        if is_asking_for_example(user_input):
            continue

        if is_asking_for_exploration(user_input):
        # is_asking_for_exploration(user_input) #outputs bool. user should start with "explore db <dataname>" to access

            continue
        else:
            continue

if __name__ == "__main__":
    main()