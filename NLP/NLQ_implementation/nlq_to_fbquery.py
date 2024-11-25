import re

def puctuation_remover(sample_nlq): 
    nlq = sample_nlq.replace(",","")
    nlq = nlq.replace("!","")
    nlq = nlq.replace("'","")
    return nlq 

class fb_nlq_parser: 
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
        
        self.curl_set = ['GET','POST','PATCH', 'get', 'post', 'patch'] 
        self.filter_set = ['orderBy','startAt','endAt','equalTo', 'orderby', 'startat', 'endat', 'equalto']#, 'range', 'between']

        self.nlq_tokens = None


    def check_orderBy(self, sample_nlq): #one attrs ONLY #was called check_attrs
        sample_nlq = puctuation_remover(sample_nlq) 
        self.nlq_tokens = sample_nlq.split(" ")  
        atts_ = {} 
        for _, i in enumerate(self.full_att_list.values()): 
            for j in i: 
                if j in self.nlq_tokens:  
                    atts_[j] = self.nlq_tokens.index(j)   
        
        if len(atts_) == 0: 
            return ValueError(f"You must include valid attribute names: {self.full_att_list}")  
        elif len(atts_) > 1:
            return ValueError(f"You wanted {atts_}. \n \tWe only accept one attribute names at a time: {self.full_att_list}")  

        result = next(iter(atts_))
        if self.does_dataset_have_attri(sample_nlq, result):
            pass
        else:
            return ValueError(f"Chosen dataset {self.check_from} does not have {atts_} attribute.")

        return f'"{result}"'
    

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
    
    def check_groupby(self, sample_nlq): #just a sample func.
        pattern = r'\b(?:group|group by|grouped|each)\b' 
        atts_position = self.check_atts(sample_nlq)
        match = re.search(pattern, sample_nlq, re.IGNORECASE)
        if match:  
            target_att_by = self.next_token(match.group(), atts_position) 
            return f"{target_att_by}"
        else:
            return None

    def check_limitTo(self, sample_nlq): #limitToFirst, limitToLast
        def extract_limitToFirst(sample_nlq):
            pattern = r'\b(?:top|highest|first)\b (\d+)' #only allows digits
            match = re.search(pattern, sample_nlq, re.IGNORECASE)
            if match:
                limit_output = match.group(1).strip()
                # print(f"limitToFirst: {limit_output}")
                result = f"limitToFirst={limit_output}"
                # self.query_parts['LIMIT'] = limit_output
                return result
            pass
        def extract_limitToLast(sample_nlq):
            pattern = r'\b(?:bottom|lowest|last)\b (\d+)' #only allows digits
            match = re.search(pattern, sample_nlq, re.IGNORECASE)
            if match:
                limit_output = match.group(1).strip()
                # print(f"limitToLast: {limit_output}")
                result = f"limitToLast={limit_output}"
                # self.query_parts['LIMIT'] = limit_output
                return result
            pass
        result = extract_limitToFirst(sample_nlq)
        result = extract_limitToLast(sample_nlq)
        return result

    def does_dataset_have_attri(self, sample_nlq, attri) -> bool:
        dataset = self.check_from(sample_nlq)
        if attri in self.full_att_list[dataset]:
            # Convert both sides to lowercase for case-insensitive comparison
            return attri.lower() in [x.lower() for x in self.full_att_list[dataset]]
        return False


    def check_equalTo(self, sample_nlq): #this is difficult. Might need help
        pattern = r'\b(?:equal to|equals to|equals|equal)\b\s+(\w+)'
        
        match = re.search(pattern, sample_nlq, re.IGNORECASE)
        if match:
            equal_value = match.group(1).strip()
            # If it's a number, don't add quotes
            if equal_value.isdigit():
                result = f'equalTo={equal_value}'
            # If it's a string, add quotes
            else:
                result = f'equalTo="{equal_value}"'
            return result
        return None

    def check_startAt(self, sample_nlq): #only with number attributes #because we do not have attributes that work in a logical sense as alphabeticle order
        start_pattern = r'\b(?:startat|start at|start)\b'
        start_match = re.search(start_pattern, sample_nlq, re.IGNORECASE)
        
        if start_match:
            start_pos = start_match.end()
            
            remaining_text = sample_nlq[start_pos:]
            value_pattern = r'(?:\d{4}-\d{2}-\d{2})|(?:\d{4}/\d{2}/\d{2})'
            value_match = re.search(value_pattern, remaining_text)
            
            if value_match:  #check for full date first
                start_value = value_match.group(0)  # Using group(0) to get entire match                
                if start_value.isdigit():
                    result = f'startAt={start_value}'
                else: #always date
                    start_value = start_value.replace('/', '-')  # Standardize separator
                    result = f'startAt={start_value}'
                return result

            value_pattern = r'(?:\b\d+\b)'
            value_match = re.search(value_pattern, remaining_text)
            
            if value_match: #check for number only
                start_value = value_match.group(0)  # Using group(0) to get entire match
                
                if start_value.isdigit():
                    result = f'startAt={start_value}'
                else:
                    start_value = start_value.replace('/', '-')  # Standardize separator
                    result = f'startAt="{start_value}"'
                return result
            
            else:
                return ValueError(f"No numerical value or date is found after 'start'.")
                
        return None

    def check_endAt(self, sample_nlq): #only with number attributes
        start_pattern = r'\b(?:endat|end at|end)\b'
        start_match = re.search(start_pattern, sample_nlq, re.IGNORECASE)
        
        if start_match:
            start_pos = start_match.end()
            
            remaining_text = sample_nlq[start_pos:]
            value_pattern = r'(?:\d{4}-\d{2}-\d{2})|(?:\d{4}/\d{2}/\d{2})'
            value_match = re.search(value_pattern, remaining_text)
            
            if value_match:  #check for full date first
                start_value = value_match.group(0)  # Using group(0) to get entire match                
                if start_value.isdigit():
                    result = f'endAt={start_value}'
                else: #always date
                    start_value = start_value.replace('/', '-')  # Standardize separator
                    result = f'endAt={start_value}'
                return result

            value_pattern = r'(?:\b\d+\b)'
            value_match = re.search(value_pattern, remaining_text)
            
            if value_match: #check for number only
                start_value = value_match.group(0)  # Using group(0) to get entire match
                
                if start_value.isdigit():
                    result = f'startAt={start_value}'
                else:
                    start_value = start_value.replace('/', '-')  # Standardize separator
                    result = f'startAt="{start_value}"'
                return result
            
            else:
                return ValueError(f"No numerical value or date is found after 'end'.")
                
        return None

    def is_attribute_number(): #for classifying diff. types of attri.
        pass

        
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
        
class NLQtoFBConverter():
    def __init__(self, sample_nlq=None):
        self.base_url = "https://dsci551-2f357-default-rtdb.firebaseio.com/"
        self.fb_nlq_parer = fb_nlq_parser()
        self.prettify = True
        # self.query_parts = {}
        pass
        

    def output_query(self, user_input):
        
        contructed_query = self.build_query(user_input)
        # print("\n*********************************************")
        # print("User Input: ", user_input)
        # print("FB Query: ", contructed_query )
        return contructed_query

    def build_query(self, user_input):

        dataset = self.fb_nlq_parer.check_from(user_input)
        order_by = self.fb_nlq_parer.check_orderBy(user_input)

        fb_query = f'curl "{self.base_url}{dataset}.json?orderBy={order_by}'

        if self.fb_nlq_parer.check_equalTo(user_input):
            fb_query += f"&{self.fb_nlq_parer.check_equalTo(user_input)}"
        if self.fb_nlq_parer.check_startAt(user_input):
            fb_query += f"&{self.fb_nlq_parer.check_startAt(user_input)}"
        if self.fb_nlq_parer.check_endAt(user_input):
            fb_query += f"&{self.fb_nlq_parer.check_endAt(user_input)}"
        if self.fb_nlq_parer.check_limitTo(user_input):
            fb_query += f"&{self.fb_nlq_parer.check_limitTo(user_input)}"
        if self.prettify:
            fb_query += f'&print=pretty"'

        
        return fb_query



#f'curl "{base_url}CDC.json?orderBy="date"&startAt="2024-01-01"&endAt="2024-03-01"&limitToFirst=50&print=pretty"'
#f'curl "{base_url}CDC.json?orderBy="state"&equalTo="CA"&limitToLast=100&print=pretty"'

def main():
    # Sample queries for testing
    sample_queries = [
        # "Show last 10 income values from FRED",
        # "Show last 10 income values from FRED start from 2024-01-01 ",
        "Show last 10 income values from FRED start from 2024-01-01 end to 2024-02-03",        
        # "Show income values form FRED"
    ]

    # Test both parsers
    print("Testing fb_nlq_parser:")
    checker = fb_nlq_parser()
    for query in sample_queries:
        print("\nQuery:", query)
        try: 
            print("Dataset: ", checker.check_from(query)) #done
            print("orderBy: ", checker.check_orderBy(query)) #done
            print("limitto___: ", checker.check_limitTo(query)) #done
            print("equalTo: <skip>", checker.check_equalTo(query)) #done
            print("startAt: ", checker.check_startAt(query)) # we don't have the ability to process from ___ to ___
            print("endAt: ", checker.check_endAt(query)) #we also did not check if attribute can actually use this query.
            print("pretty print by default: print=pretty")

        except ValueError as e:
            print("Error:", str(e))

    converter = NLQtoFBConverter()
    for query in sample_queries:
        converter.output_query(query) #print constructed query.


if __name__ == "__main__":
    main()