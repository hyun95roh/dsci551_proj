import re

def match_attributes(sentence, attribute_sets):
    # Preprocess the sentence
    sentence = sentence.lower()
    words = set(re.findall(r'\b\w+\b', sentence))
    
    matched_sets = {}
    
    for set_name, attributes in attribute_sets.items():
        matched_attributes = []
        for attr in attributes:
            # Preprocess the attribute
            attr_lower = attr.lower()
            
            # Check for exact match
            if attr_lower in sentence:
                matched_attributes.append(attr)
        
        if matched_attributes:
            matched_sets[set_name] = matched_attributes
    
    return matched_sets

###############################################################################################
# # Example usage
# attributes = [
#     "Real Median Household Income",
#     "Population Percentage below 100 FPL",
#     "Unemployment Rate",
#     "Median Age",
#     "Total Population"
# ]

# sentence = "What is the average of Real Median Household Income when the population percentage below 100 percentage FPL exceeds 30"

# matched = match_attributes(sentence, attributes)
# # print(f"Matched attributes: {matched}")
###############################################################################################
