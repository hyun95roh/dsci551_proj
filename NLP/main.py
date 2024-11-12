from attribute_matcher import match_attributes
from attribute_sets import attribute_sets


sentence = "What is the average of Real Median Household Income when the population percentage below 100 percentage FPL exceeds 30"

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


def main():
    while True:
        user_input = input("Enter your query (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        print(f"Your Input: {user_input}")
        print()

if __name__ == "__main__":
    main()