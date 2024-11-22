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
base_url = 'https://dsci551-2f357-default-rtdb.firebaseio.com/'


def is_asking_sql_example(user_input) -> bool:
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
            if keyword == "groupby":
                response = template_groupby()
            elif keyword == "having":
                response = template_having()
            elif keyword == "where":
                response = template_where()
            elif keyword == "orderby":
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
    # Make input case-incensitive and space-incensitive.
    user_input = user_input.lower().replace(" ","") 
    #just ignore join for now
    keyword_sets = {"where", "groupby", "having", "orderby", "aggregation"}
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
    output = f"SELECT CAST(AVG({random_select}) AS FLOAT) FROM {random_database} GROUP BY {random_groupby};"
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
        sample_having = ["SELECT LEFT(DATE,4) AS YEAR, COUNT(*) as record_count FROM STOCK GROUP BY YEAR HAVING YEAR='2020';",
                         "SELECT LEFT(DATE,4) AS YEAR, AVG(NOV) as avg_price FROM STOCK GROUP BY YEAR HAVING YEAR like '201%';",
                         "SELECT LEFT(DATE,4) AS YEAR, AVG(NOV), AVG(LLY) as avg_price FROM STOCK WHERE LEFT(DATE,4) like '200%' GROUP BY LEFT(DATE,4) ;"
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
    database_var = ["CDC","FRED","STOCK"]
    random_database = random.choice(database_var)

    if random_database == "CDC":
        sample_where = [
                "SELECT SUBTOPIC, CLASSIFICATION FROM CDC WHERE SUBTOPIC_ID = 1;",
                "SELECT GROUP_NAME, ESTIMATE FROM CDC WHERE ESTIMATE_TYPE_ID = 2 AND TIME_PERIOD = '2015-2018';",
                "SELECT * FROM CDC WHERE SUBGROUP_ID = 9 AND CLASSIFICATION_ID = 3;"
            ]

    elif random_database == "FRED":
        sample_where = [
                "SELECT date, income FROM FRED WHERE income > 70000;",
                "SELECT date, income FROM FRED WHERE date = '01/01/2010';",
                "SELECT * FROM FRED WHERE income BETWEEN 60000 AND 80000;"
            ]

    elif random_database == "STOCK":
        sample_where = [
                "SELECT date, NOV, LLY FROM STOCK WHERE date like '2010-06%';",
                "SELECT * FROM STOCK WHERE date like '2020-01%';",
                "SELECT date, NOV, LLY FROM STOCK WHERE LLY BETWEEN 60 AND 120;"
            ]

    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:")
    output = random.choice(sample_where)  
    print( output )
    return output 
    

def template_orderby(): 
    database_var = ["CDC","FRED","STOCK"]
    random_database = random.choice(database_var)

    if random_database == "CDC":
        sample_where = [
                "SELECT SUBTOPIC, CLASSIFICATION FROM CDC WHERE SUBTOPIC_ID = 1 ORDER BY SUBTOPIC DESC;",
                "SELECT GROUP_NAME, ESTIMATE FROM CDC WHERE TIME_PERIOD like '201%' ORDER BY GROUP_NAME;",
                "SELECT * FROM CDC WHERE SUBGROUP_ID = 9 AND CLASSIFICATION_ID = 3 ORDER BY ESTIMATE DESC;"
            ]

    elif random_database == "FRED":
        sample_where = [
                "SELECT date, income FROM FRED WHERE income > 70000 ORDER BY income DESC;",
                "SELECT date, income FROM FRED WHERE date = '01/01/2010' ORDER BY date;",
                "SELECT * FROM FRED WHERE income BETWEEN 60000 AND 80000 ORDER BY income DESC;"
            ]

    elif random_database == "STOCK":
        sample_where = [
                "SELECT date, NOV, LLY FROM STOCK WHERE date like '2010%' ORDER BY date;",
                "SELECT * FROM STOCK WHERE date like '2020%' ORDER BY date;",
                "SELECT date, NOV, LLY FROM STOCK WHERE LLY BETWEEN 60 AND 120 ORDER BY date DESC;"
            ]

    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:")
    output = random.choice(sample_where)  
    print( output )
    return output     

def template_aggregation(keyword):
    aggregation_numbers_sets = {"sum", "min", "max", "avg"} 
    database_var = ["CDC","FRED","STOCK"] 
    random_database = random.choice(database_var) 

    if random_database == "CDC":
        sample_where = [
                "SELECT SUBTOPIC, COUNT(CLASSIFICATION) FROM CDC GROUP BY SUBTOPIC ORDER BY SUBTOPIC DESC;",
                "SELECT GROUP_NAME, MAX(ESTIMATE) FROM CDC GROUP BY GROUP_NAME ORDER BY GROUP_NAME;",
                "SELECT AVG(ESTIMATE) FROM CDC ORDER BY AVG(ESTIMATE) DESC;"
            ]

    elif random_database == "FRED":
        sample_where = [
                "SELECT RIGHT(date,4) AS YEAR, CAST(AVG(income) AS FLOAT) AS avg_income  FROM FRED WHERE income > 70000 GROUP BY YEAR ORDER BY AVG(income) DESC;",
                "SELECT RIGHT(date,4) AS YEAR, MIN(income) FROM FRED WHERE date like '%2010' GROUP BY YEAR ORDER BY YEAR;",
                "SELECT RIGHT(date,4) AS YEAR, SUM(income) FROM FRED WHERE income BETWEEN 60000 AND 80000 GROUP BY YEAR ORDER BY SUM(income) DESC;"
            ]

    elif random_database == "STOCK":
        sample_where = [
                "SELECT LEFT(date,4) AS YEAR, AVG(NOV), AVG(LLY) FROM STOCK GROUP BY YEAR HAVING YEAR like '2010%' ORDER BY YEAR;",
                "SELECT LEFT(date,4) AS YEAR, MAX(NOV), MAX(LLY) FROM STOCK GROUP BY YEAR HAVING YEAR like '2020%' ORDER BY YEAR;",
                "SELECT LEFT(date,4) AS YEAR, MIN(NOV), MIN(LLY) FROM STOCK GROUP BY YEAR HAVING YEAR like '2000%' ORDER BY YEAR DESC;"
            ]

    else:
        print("if you see this something went horribly wrong.")
        return

    print("EXAMPLE QUERY:")
    output = random.choice(sample_where)  
    print( output )
    return output
    
def is_asking_fire_example(user_input) ->bool: 
    user_input = user_input.lower()
    if "example query" in user_input: 
        #IS asking for example query
        print("You are asking for example query...")

        keywords = what_keyword_fire(user_input)
        print(f"You are asking for example query of {keywords} \n")

        response = "" 
        for keyword in keywords:
            if keyword == "GET":
                response = template_get()
            elif keyword == "orderBy":
                response = template_orderby() 
            elif keyword in ["startAt", "endAt", "equalTo", "between"]:
                response = template_range() 
            elif keyword == "limit" or keyword in ['limitToFirst','limitToLast']:  
                response = template_limit()  
            else:
                pass

        #output template of query based on keywords
        return True, response
    else:
        print("Available format: example query <GET|orderBy|startAt|endAt|equalTo|limitToFirst|limitToLast>")
        return False, ""
    
def what_keyword_fire(user_input):
    user_input = user_input  
    selected_keywords = [] 

    curl_set = ['GET','POST','PATCH', 'get', 'post', 'patch'] 
    filter_set = ['orderBy','startAt','endAt','equalTo', 'orderby', 'startat', 'endat', 'equalto'] 

    for i in curl_set: 
        if i in user_input :
            selected_keywords.append(i.upper()) # Uppercase-sensitive

    for i in filter_set: 
        if i in user_input: 
            q1 = i[-2:] 
            q2 = q1[0].upper() + q1[1] 
            j = i.replace(q1, q2)  
            selected_keywords.append(j)

    return selected_keywords 

def template_get(): 
    sample_get = [
        f'curl "{base_url}FRED.json"',
        f'curl "{base_url}STOCK.json"',
        f'curl "{base_url}CDC.json"'
    ]

    print("EXAMPLE QUERY:")
    output = random.choice(sample_get)   
    print( output )
    return output

def template_limit():
    sample_limit = [
        f'curl {base_url}/FRED.json?limitToFirst=5',
        f'curl {base_url}/STOCK.json?limitToLast=1',
        f'curl {base_url}/CDC.json?limitToFirst=5'
    ]
    print("EXAMPLE QUERY:")
    output = random.choice(sample_limit)   
    print( output )
    return output
