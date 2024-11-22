import re
import pandas as pd

def puctuation_remover(sample_nlq): 
    nlq = sample_nlq.replace(",","")
    nlq = nlq.replace("!","")
    nlq = nlq.replace("'","")
    return nlq 

class nlq_parser: 
    def __init__(self, sample_nlq=None):
        self.nlq = sample_nlq 
        self.full_table_list = ['FRED', 'CDC', 'STOCK']  
        self.full_att_list = {
            'FRED': ['date','income'], 
            'STOCK': ['DATE','NOV','LLY'],
            'CDC': ['SUBTOPIC', 'SUBTOPIC_ID', 'CLASSIFICATION', 'CLASSIFICATION_ID', 
                   'GROUP_NAME', 'GROUP_ID', 'SUBGROUP', 'SUBGROUP_ID', 'ESTIMATE_TYPE', 
                   'ESTIMATE_TYPE_ID', 'TIME_PERIOD', 'TIME_PERIOD_ID', 'ESTIMATE', 
                   'STANDARD_ERROR']
        } 
        
        self.nlq_start_token = ["find", "group", "show", "retrieve", "calculate", 
                               "identify", "count", "list", "display", "tell"]
        self.nlq_agg_token = ['sum', 'total', 'average', 'mean', 'max', 'min']
        self.nlq_tokens = None

    def check_atts(self, sample_nlq): 
        sample_nlq = puctuation_remover(sample_nlq) 
        self.nlq_tokens = sample_nlq.split(" ")  
        atts_ = {} 
        for _, i in enumerate(self.full_att_list.values()): 
            for j in i: 
                if j in self.nlq_tokens:  
                    atts_[j] = self.nlq_tokens.index(j)   
        
        if len(atts_) == 0: 
            return ValueError(f"You must include valid attribute names: {self.full_att_list}")  
        return atts_ 

    def check_from(self, sample_nlq): 
        found_table = False
        from_ = ""#"FROM " 
        for i in self.full_table_list:
            if i in sample_nlq and i not in from_:
                from_ = from_ + i + ","
                found_table = True
    
        if not found_table:
            return ValueError(f"Your query must include at least one valid table name: {', '.join(self.full_table_list)}")
        
        from_ = from_[:-1]
        return from_ 

    def check_select(self, sample_nlq):
        cnt = 0
        pattern = r'\b(?:find|display|show|list|identify|retrieve|tell|Calculate)\b'
        atts_position = self.check_atts(sample_nlq)
        match = re.search(pattern, sample_nlq, re.IGNORECASE)
        if match:    
            cnt += 1 

        if cnt == 0: 
            return ValueError("Your query must include at least one word: 'display','show','list','identify','retrieve','tell'.")
        else:
            target_atts = self.adjacent_token(match.group(), atts_position) 
            return f"{target_atts}" #f"SELECT {target_atts}"
        
    def check_groupby(self, sample_nlq): 
        pattern = r'\b(?:group|group by|grouped|each)\b' #can not take two word keywords
        atts_position = self.check_atts(sample_nlq)
        match = re.search(pattern, sample_nlq, re.IGNORECASE)
        if match:  
            target_att_by = self.next_token(match.group(), atts_position) 
            return f"{target_att_by}"
        else:
            return None
        
    def check_aggregation(self, sample_nlq): 
        aggregation_functions = [] 
        for i in self.nlq_agg_token: 
            if i in sample_nlq: 
                aggregation_functions.append(i) 
        return aggregation_functions if aggregation_functions else None

    def adjacent_token(self, token: str, atts_position: dict, verbose=False):
        target_idx = self.nlq_tokens.index(token) #can not take two words keywords as token
        min_distance = 99999
        adjacent_token = "" 
        for k, v in atts_position.items():
            distance = abs(v - target_idx)
            if distance < min_distance:
                min_distance = distance 
                adjacent_token = k 
        if verbose == False:
            return adjacent_token
        else: 
            print(atts_position)
            print(f"Target({token}) index:", target_idx)
            return adjacent_token

    def next_token(self, token: str, atts_position: dict, verbose=False): #new function. look for NEXT instead of closest
        target_idx = self.nlq_tokens.index(token)
        min_distance = 99999
        next_token = "" 
        
        # Only look at tokens that come after the target
        for k, v in atts_position.items():
            if v > target_idx:  # Only consider positions after the keyword
                distance = v - target_idx  # Remove abs() to only look forward
                if distance < min_distance:
                    min_distance = distance 
                    next_token = k 
        
        if verbose:
            print(atts_position)
            print(f"Target({token}) index:", target_idx)
            
        return next_token

class NLQtoSQLConverter:
    def __init__(self):
        self.nlq_parser = nlq_parser() #create instance of nlq_parser

        self.keywords = {
            'select': ['find', 'list', 'show', 'display', 'identify', 'retrieve', 'calculate'],
            'from': ['in the', 'from the', 'using the'],
            'where': ['where'],
            'group by': ['group by', 'grouped by'],
            'order by': ['ordered by', 'sorted by'],
            'limit': ['top', 'highest', 'lowest', 'only']
        }
        self.query_parts = {}

    def convert_nlq_to_sql(self, nlq):
        self.query_parts = {
            'SELECT': '',
            'FROM': '',
            'WHERE': '',
            'GROUP BY': '',
            'ORDER BY': '',
            'LIMIT': ''
        }
        
        # self.extract_select_clause(nlq)
        self.extract_select_clause2(nlq)
        # self.extract_from_cålause(nlq)
        self.extract_from_clause2(nlq)
        
        self.extract_where_clause(nlq)

        # self.extract_group_by_clause(nlq)
        self.extract_group_by_clause2(nlq)

        self.extract_order_by_clause(nlq)

        self.extract_limit_clause(nlq)

        print("\n")
        # self.extract_aggregation_clause2(nlq) #this included in select
        
        return self.build_sql_query()

    def extract_select_clause(self, nlq):
        pattern = r'\b(?:' + '|'.join(self.keywords['select']) + r')\b (.+?) \b(?:' + '|'.join(self.keywords['from']) + r')\b'
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            self.query_parts['SELECT'] = match.group(1).strip()
        else:
            raise ValueError("No SELECT clause found in the query.")

    def extract_select_clause2(self, nlq):
        first_aggregation_output = self.extract_aggregation_clause2(nlq)
        select_output = self.nlq_parser.check_select(nlq)

        if first_aggregation_output:
            first_aggregation_output = first_aggregation_output.upper()
            print(f"Select: SELECT {first_aggregation_output}({select_output})")
            self.query_parts['SELECT'] = f"{first_aggregation_output}({select_output})"

        else:
            print("Select:",  self.nlq_parser.check_select(nlq))
            self.query_parts['SELECT'] = f"{select_output}"

    def extract_from_clause(self, nlq):
        pattern = r'\b(?:' + '|'.join(self.keywords['from']) + r')\b (\w+)'
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            self.query_parts['FROM'] = match.group(1).strip()
        else:
            raise ValueError("No FROM clause found in the query.")

    def extract_from_clause2(self, nlq):
        from_output = self.nlq_parser.check_from(nlq)
        print("From:", self.nlq_parser.check_from(nlq))
        self.query_parts['FROM'] = f"{from_output}"

    def extract_where_clause(self, nlq):
        # pattern = r'\b(?:where)\b'
        pattern = r'\bwhere\b (.+?)(?=\b(?:' + '|'.join(self.keywords['group by'] + self.keywords['order by'] + self.keywords['limit']) + r')\b|$)'
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            where_output = match.group(1).strip()
            where_output = self.convert_to_query_syntax(where_output)
            print(f"Where: {where_output}")
            self.query_parts['WHERE'] = where_output

    def convert_to_query_syntax(self, condition_str):
        # Dictionary mapping natural language to SQL operators
        operator_mapping = {
            'equals': '=',
            'equal': '=',
            'is': '=',
            'greater than': '>',
            'bigger than': '>',
            'more than': '>',
            'larger than': '>',
            'less than': '<',
            'smaller than': '<',
            'lesser than': '<',
            'not equal': '!=',
            'not equals': '!=',
            'greater than or equal': '>=',
            'bigger than or equal': '>=',
            'less than or equal': '<=',
            'smaller than or equal': '<=',
            'like': 'LIKE',
            'contains': 'LIKE'
        }
        
        # Split the condition into words
        words = condition_str.lower().split()
        
        if len(words) < 3:
            return None
        
        field = words[0]
        value = words[-1]
        
        # Join the middle words to handle multi-word operators
        operator_text = ' '.join(words[1:-1])
        
        # Try to find the operator in our mapping
        operator = operator_mapping.get(operator_text)
        
        if operator:
            # Handle LIKE operator specially
            if operator == 'LIKE':
                return f"{field} LIKE '%{value}%'"
            # For numeric values, don't add quotes
            if value.replace('.', '').isdigit():
                return f"{field} {operator} {value}"
            # For string values, add quotes
            return f"{field} {operator} '{value}'"
        
        return None

    def extract_group_by_clause(self, nlq):
        pattern = r'\b(?:group by|grouped by)\b (.+?)(?=\b(?:' + '|'.join(self.keywords['order by'] + self.keywords['limit']) + r')\b|$)'
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            self.query_parts['GROUP BY'] = match.group(1).strip()

    def extract_group_by_clause2(self, nlq):
        groupby_output = self.nlq_parser.check_groupby(nlq)
        print("Group By:", self.nlq_parser.check_groupby(nlq))
        if groupby_output == None:
            return
        else:
            self.query_parts['GROUP BY'] = f"{groupby_output}"

    def extract_order_by_clause(self, nlq):
        pattern = r'\b(?:ordered by|sorted by)\b (.+?)(?=\b(?:' + '|'.join(self.keywords['limit']) + r')\b|$)'
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            orderby_output = match.group(1).strip()
            orderby_output = self.convert_to_order_syntax(orderby_output)
            print(f"Order By: {orderby_output}")
            self.query_parts['ORDER BY'] = orderby_output

    def convert_to_order_syntax(self, order_str):
        # Dictionary mapping natural language to SQL order terms
        order_mapping = {
            'ascending': 'ASC',
            'asc': 'ASC',
            'increasing': 'ASC',
            'up': 'ASC',
            'descending': 'DESC',
            'desc': 'DESC',
            'decreasing': 'DESC',
            'down': 'DESC',
            'newest': 'DESC',
            'latest': 'DESC',
            'highest': 'DESC',
            'largest': 'DESC',
            'oldest': 'ASC',
            'earliest': 'ASC',
            'smallest': 'ASC',
            'lowest': 'ASC'
        }
        
        # Split the string and convert to lowercase
        words = order_str.lower().split()
        
        if len(words) < 2:
            return None
            
        # First word(s) are the field name until the last word
        field = ' '.join(words[:-1])
        order_term = words[-1]
        
        # Get the SQL order direction
        direction = order_mapping.get(order_term)
        
        if direction:
            return f"{field} {direction}"
        
        return None

    def extract_limit_clause(self, nlq):
        pattern = r'\b(?:top|highest|lowest|only)\b (\d+)' #only allows digits
        match = re.search(pattern, nlq, re.IGNORECASE)
        if match:
            limit_output = match.group(1).strip()
            print(f"Limit: {limit_output}")
            self.query_parts['LIMIT'] = limit_output

    def extract_aggregation_clause2(self, nlq):
        try:
            aggregation_output = self.nlq_parser.check_aggregation(nlq)
            print("Aggregation:", self.nlq_parser.check_aggregation(nlq)[0])
            return aggregation_output[0]
        except:
            return None


    def build_sql_query(self):
        sql_query = f"SELECT {self.query_parts['SELECT']} FROM {self.query_parts['FROM']}"

        if self.query_parts['WHERE']:
            sql_query += f" WHERE {self.query_parts['WHERE']}"
        if self.query_parts['GROUP BY']:
            sql_query += f" GROUP BY {self.query_parts['GROUP BY']}"
        if self.query_parts['ORDER BY']:
            sql_query += f" ORDER BY {self.query_parts['ORDER BY']}"
        if self.query_parts['LIMIT']:
            sql_query += f" LIMIT {self.query_parts['LIMIT']}"
        
        return sql_query

def main():
    # Sample queries for testing
    sample_queries = [
        # "Find the sum income from FRED.",   #THIS WORKS!
        #                                     #NOTE: the word "total" should be sum, but would be confused with aggregation "total".
        #                                     #avoid this word for now.
        #                                     #if we want to actually allow the user to use total, maybe let them try "total instance of" instead

        # "Show the average income by date from FRED.", #THIS WORKS!
        # "List all NOV and LLY values from STOCK.",  #DOES NOT WORK (only first NOV)
        #                                             # NOTE: can not differentiate between attributes of other keywords, or they want two SELECTS.
        #                                             # no workaround so far. maybe we only accept two selects when there is no other query keywords? 
                                                     
        # "Display the sum of ESTIMATE grouped by GROUP_NAME in CDC.", #THIS WORKS!
        # "Calculate the max STANDARD_ERROR for each ESTIMATE_TYPE in CDC.", #DOES NOT WORk. wayyy to hard
        # "Identify the min income from FRED.", #THIS WORKS!
        # "Identify the TIME_PERIOD Group and by SUBGROUP in CDC.", #THIS WORKS!
        # "Tell me the mean income for each date in FRED.", #THIS WORKS!
        # "Find the total ESTIMATE for each TIME_PERIOD_ID in CDC.",   #THIS WORKS! 
                              
        #                                       #NOTE: the word "total" should be sum
        # "Find income from FRED where date equals 2024", #THIS WORKS!
        # "Show me ESTIMATE from CDC where ESTIMATE bigger than 30", #THIS WORKS!
        # "List NOV from STOCK ordered by  DATE descending", #order by #THIS WORKS!
        # "List NOV from STOCK where date is 2024 ordered by DATE descending", #combine wher and order by #THIS WORKS!

        "Show top 5 income values from FRED", #limit
    ]

    # Test both parsers
    print("Testing nlq_parser:")
    checker = nlq_parser()
    for query in sample_queries:
        print("\nQuery:", query)
        try:
            print("Attributes:", checker.check_atts(query))
            print("Select:", checker.check_select(query))
            print("From:", checker.check_from(query))
            print("Group By:", checker.check_groupby(query))
            print("Aggregation:", checker.check_aggregation(query))
        except ValueError as e:
            print("Error:", str(e))

    print("\nTesting NLQtoSQLConverter:")
    converter = NLQtoSQLConverter()
    for query in sample_queries:
        print("\nQuery:", query)
        try:
            sql_query = converter.convert_nlq_to_sql(query)
            sql_query = sql_query + ";"
            print("SQL:", sql_query)
        except ValueError as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()
