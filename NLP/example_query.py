"""
SQL Example Generator

This script generates random SQL query examples based on user input text.
Supports GROUP BY, HAVING, WHERE, ORDER BY, and aggregation functions using
sample data from mock CDC and FRED databases.

Usage:
    from sql_example_generator import is_asking_for_example

    # Generate a GROUP BY example
    is_asking_for_example("example query for group by")

    # Generate multiple examples
    is_asking_for_example("example query for group by and having")

    # Generate aggregation example
    is_asking_for_example("example query for sum")

Supported Keywords:
    - Basic: where, group by, having, order by
    - Aggregations: sum, min, max, count, avg

Sample Databases:
    - CDC: Health and weight-related statistics
    - FRED: Federal Reserve economic data
"""

import re
import random


def is_asking_for_example(user_input) -> bool:
    #testing input
    # user_input = "example query for order by"

    user_input = user_input.lower()
    if "example query" in user_input: 
        #IS asking for example query
        print("You are asking for example query...")

        keywords = what_keyword(user_input)
        print(f"You are asking for example query of {keywords} \n")

        response = "" 
        for keyword in keywords:
            if keyword == "group by":
                response = template_groupby()
            elif keyword == "having":
                response = template_having()
            elif keyword == "where":
                response = template_where()
            elif keyword == "order by":
                response = template_orderby()
            elif keyword == "aggregation" or keyword in {"sum", "min", "max", "count", "avg"}:  
                response = template_aggregation(keyword)

            else:
                pass

        #output template of query based on keywords
        return True, response
    else:
        print("You are NOT asking for example query")
        return False, "" 


def what_keyword(user_input):
    user_input = user_input.lower()
    #just ignore join for now
    keyword_sets = {"where", "group by", "having", "order by", "aggregatation"}
    aggregation_sets = {"sum", "min", "max", "count", "avg"}

    selected_keywords = []

    for keyword in keyword_sets:
        if keyword in user_input:
            selected_keywords.append(keyword)

    for keyword in aggregation_sets:
        if keyword in user_input:
            selected_keywords.append(keyword)


    return selected_keywords #supports multiple selection of keywords

def template_groupby():
    database_var = ["CDC","FRED","STOCK"]
    random_database = random.choice(database_var)

    if random_database == "CDC":
        '''
        #CDC_database_attributes = {
        #four attributes
        "subtopic": ["normal_weight", "overweight", 
                     "obese", "grade_1_obese", 
                     "grade_2_obese", "grade_3_obses"], #6 options
        "subgroup": ["below_100%_FPL", "100%_to_199%_FPL", 
                     "200%_to_399%_FPL", "above_400%_FPL"], #4 options
        "estimate_type": ["age", "crude"], #2 options
        "time_period": ["1988_to_1994", "1999_to_2002", 
                        "2003_to_2006", "2007_to_2010", 
                        "2011_to_2014", "2015_to_2018"] #6 options
        }''' 
        CDC_database_attributes = ['SUBTOPIC','SUBTOPIC_ID','CLASSIFICATION','CLASSIFICATION_ID',
                                   'GROUP_NAME','GROUP_ID','SUBGROUP','SUBGROUP_ID',
                                   'ESTIMATE_TYPE','ESTIMATE_TYPE_ID',
                                   'TIME_PERIOD','TIME_PERIOD_ID','ESTIMATE', 'TIME_PERIOD_ID']  
        random_select = random.choice(CDC_database_attributes)  
        random_groupby = random.choice([i for i in CDC_database_attributes if i not in random_select]) 

    elif random_database == "FRED":
        FRED_database_attributes = ['date','income']   
        random_select = random.choice(FRED_database_attributes)  
        random_groupby = random.choice([i for i in FRED_database_attributes if i not in random_select])

    elif random_database == "STOCK":
        STOCK_database_attributes = ['DATE','NOV','LLY']    
        random_select = random.choice(STOCK_database_attributes)  
        random_groupby = random.choice([i for i in STOCK_database_attributes if i not in random_select])


    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:\n")
    output = f"SELECT AVG({random_select}) FROM {random_database} GROUP BY {random_groupby};"
    print(output) 
    return output 
    

def template_having():
    database_var = ["STOCK"] #"FRED","STOCK" 
    random_database = random.choice(database_var)

    if random_database == "CDC":
        '''
        CDC_database_attributes = ['SUBTOPIC','SUBTOPIC_ID','CLASSIFICATION','CLASSIFICATION_ID',
                                   'GROUP_NAME','GROUP_ID','SUBGROUP','SUBGROUP_ID',
                                   'ESTIMATE_TYPE','ESTIMATE_TYPE_ID',
                                   'TIME_PERIOD','TIME_PERIOD_ID','ESTIMATE', 'TIME_PERIOD_ID']  
        random_select = random.choice(CDC_database_attributes)  
        random_groupby = random.choice([i for i in CDC_database_attributes if i not in random_select]) 
        '''
        sample_having = ["SELECT GROUP_NAME, AVG(ESTIMATE) AS avg_estimate FROM CDC GROUP BY GROUP_NAME HAVING AVG(ESTIMATE) < 50;",
                      "SELECT SUBTOPIC, SUM(ESTIMATE) AS total_estimate FROM CDC GROUP BY SUBTOPIC HAVING SUM(ESTIMATE) > 10;",
                      "SELECT TIME_PERIOD, COUNT(DISTINCT GROUP_ID) AS distinct_groups FROM CDC GROUP BY TIME_PERIOD HAVING COUNT(DISTINCT GROUP_ID) > 1;"        
                      ]

    elif random_database == "FRED":
        '''
        FRED_database_attributes = ['date','income']   
        random_select = random.choice(FRED_database_attributes)  
        random_groupby = random.choice([i for i in FRED_database_attributes if i not in random_select])
        '''
        sample_having = ["SELECT date, COUNT(*) AS record_count FROM FRED GROUP BY date HAVING COUNT(*) > 2;", 
                         "SELECT income, AVG(income) AS average_income FROM FRED GROUP BY income HAVING AVG(income) > 50000;",
                         "SELECT date, SUM(income) AS total_income FROM FRED GROUP BY date HAVING SUM(income) > 200000;"
                        ]
        
    elif random_database == "STOCK":
        '''
        STOCK_database_attributes = ['DATE','NOV','LLY']    
        random_select = random.choice(STOCK_database_attributes)  
        random_groupby = random.choice([i for i in STOCK_database_attributes if i not in random_select])
        '''
        sample_having = ["SELECT DATE, COUNT(*) as transaction_count FROM STOCK GROUP BY DATE HAVING COUNT(*) >= 1;",
                         "SELECT NOV, SUM(price) as total_price FROM STOCK GROUP BY NOV HAVING SUM(price) > 1000;"
                         "SELECT LLY, AVG(price) as avg_price FROM STOCK GROUP BY LLY HAVING AVG(price) < 50;"
                        ]
        
    else:
        print("if you see this something went horribly wrong.")
        return
    
    print("EXAMPLE QUERY:")
    output = random.choice(sample_having) 
    print( output )
    '''
    agg_functions = ["COUNT"]
    random_agg = random.choice(agg_functions)
    # Get random condition value for HAVING
    random_number = random.randint(1, 100)
    
    print(f"""
    SELECT {random_agg}(id) as agg_result FROM {random_database} 
    GROUP BY {random_groupby}
    HAVING {random_agg}(id) < {random_number};
    """) 
    ''' 
    return output 

def template_where():
    database_var = ["CDC","FRED"]
    random_database = random.choice(database_var)

    if random_database == "CDC":
        CDC_database_attributes = {
        #four attributes
        "subtopic": ["normal_weight", "overweight", 
                     "obese", "grade_1_obese", 
                     "grade_2_obese", "grade_3_obses"], #6 options
        "subgroup": ["below_100%_FPL", "100%_to_199%_FPL", 
                     "200%_to_399%_FPL", "above_400%_FPL"], #4 options
        "estimate_type": ["age", "crude"], #2 options
        "time_period": ["1988_to_1994", "1999_to_2002", 
                        "2003_to_2006", "2007_to_2010", 
                        "2011_to_2014", "2015_to_2018"] #6 options
        }
        random_select = random.choice(list(CDC_database_attributes.keys()))
        random_where = random.choice(CDC_database_attributes[random_select])

    elif random_database == "FRED":
        FRED_database_attributes = {
            "date": ["1980", "1990", "2000", "2010", "2020"],
            "real_median_house": ["50,000", "60,000", "70,000", 
                                  "80,000", "90,000"]
        }
        random_select = random.choice(list(FRED_database_attributes.keys()))
        random_where = random.choice(FRED_database_attributes[random_select])

    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:\n")
    print(f"SELECT {random_select} FROM {random_database} \nWHERE {random_select} = {random_where};\n")
    pass

def template_orderby(): 
    database_var = ["CDC","FRED"]
    random_database = random.choice(database_var)

    order_var = ["ASC", "DESC"]
    random_order = random.choice(order_var)

    if random_database == "CDC":
        CDC_database_attributes = {
        #four attributes
        # "subtopic": ["normal_weight", "overweight", 
        #              "obese", "grade_1_obese", 
        #              "grade_2_obese", "grade_3_obses"], #6 options
        "subgroup": ["1_below_100%_FPL", "2_100%_to_199%_FPL", 
                     "3_200%_to_399%_FPL", "4_above_400%_FPL"], #4 options
        # "estimate_type": ["age", "crude"], #2 options
        "time_period": ["1988_to_1994", "1999_to_2002", 
                        "2003_to_2006", "2007_to_2010", 
                        "2011_to_2014", "2015_to_2018"] #6 options
        }
        random_select = random.choice(list(CDC_database_attributes.keys()))
        # random_orderby = random.choice(CDC_database_attributes[random_select])

    elif random_database == "FRED":
        FRED_database_attributes = {
            "date": ["1980", "1990", "2000", "2010", "2020"],
            "real_median_house": ["50,000", "60,000", "70,000", 
                                  "80,000", "90,000"]
        }
        random_select = random.choice(list(FRED_database_attributes.keys()))
        # random_orderby = random.choice(FRED_database_attributes[random_select])

    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:\n")
    print(f"SELECT {random_select} FROM {random_database} \nORDER BY {random_select} {random_order};\n")
    pass

def template_aggregation(keyword):
    aggregation_numbers_sets = {"sum", "min", "max", "avg"}
    aggregation_count = {"count"}

    if keyword in aggregation_numbers_sets:
        database_var = ["CDC","FRED"]
        random_database = random.choice(database_var)

        if random_database == "CDC":
            CDC_database_attributes = {
            "subgroup": ["1_below_100%_FPL", "2_100%_to_199%_FPL", 
                        "3_200%_to_399%_FPL", "4_above_400%_FPL"], #4 options
            "time_period": ["1988_to_1994", "1999_to_2002", 
                            "2003_to_2006", "2007_to_2010", 
                            "2011_to_2014", "2015_to_2018"] #6 options
            }
            random_select = random.choice(list(CDC_database_attributes.keys() ))

        elif random_database == "FRED":
            FRED_database_attributes = {
                "date": ["1980", "1990", "2000", "2010", "2020"],
                "real_median_house": ["50,000", "60,000", "70,000", 
                                    "80,000", "90,000"]
            }
            random_select = random.choice(list(FRED_database_attributes.keys()))
        else:
            print("if you see this something went horribly wrong.")
            return

        print("EXAMPLE QUERY:\n")
        print(f"SELECT {keyword}({random_select}) FROM {random_database}; \n")

        pass

    elif keyword in aggregation_count:
        database_var = ["CDC","FRED"]
        random_database = random.choice(database_var)

        if random_database == "CDC":
            CDC_database_attributes = {
            #four attributes
            "subtopic": ["normal_weight", "overweight", 
                         "obese", "grade_1_obese", 
                         "grade_2_obese", "grade_3_obses"], #6 options
            "subgroup": ["1_below_100%_FPL", "2_100%_to_199%_FPL", 
                        "3_200%_to_399%_FPL", "4_above_400%_FPL"], #4 options
            "estimate_type": ["age", "crude"], #2 options
            "time_period": ["1988_to_1994", "1999_to_2002", 
                            "2003_to_2006", "2007_to_2010", 
                            "2011_to_2014", "2015_to_2018"] #6 options
            }
            random_select = random.choice(list(CDC_database_attributes.keys()))

        elif random_database == "FRED":
            FRED_database_attributes = {
                "date": ["1980", "1990", "2000", "2010", "2020"],
                "real_median_house": ["50,000", "60,000", "70,000", 
                                    "80,000", "90,000"]
            }
            random_select = random.choice(list(FRED_database_attributes.keys()))


        print("EXAMPLE QUERY:\n")
        print(f"SELECT {keyword}({random_select}) FROM {random_database}; \n")

    else:
    #just the word aggregation
        database_var = ["CDC","FRED"]
        random_database = random.choice(database_var)

        aggregation_numbers_sets = {"sum", "min", "max", "avg"}
        random_aggregation = random.choice(aggregation_numbers_sets)



        if random_database == "CDC":
            CDC_database_attributes = {
            "subgroup": ["1_below_100%_FPL", "2_100%_to_199%_FPL", 
                        "3_200%_to_399%_FPL", "4_above_400%_FPL"], #4 options
            "time_period": ["1988_to_1994", "1999_to_2002", 
                            "2003_to_2006", "2007_to_2010", 
                            "2011_to_2014", "2015_to_2018"] #6 options
            }
            random_select = random.choice(list(CDC_database_attributes.keys()))

        elif random_database == "FRED":
            FRED_database_attributes = {
                "date": ["1980", "1990", "2000", "2010", "2020"],
                "real_median_house": ["50,000", "60,000", "70,000", 
                                    "80,000", "90,000"]
            }
            random_select = random.choice(list(FRED_database_attributes.keys()))
        else:
            print("if you see this something went horribly wrong.")
            return

        print("EXAMPLE QUERY:\n")
        print(f"SELECT {random_aggregation}({random_select}) FROM {random_database}; \n")
    
