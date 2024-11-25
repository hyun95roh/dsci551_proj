import streamlit as st
import pandas as pd
import re 
import time

# Set page configuration
st.set_page_config(page_title="551 Project", page_icon="📚")


#Page 1
def page1():
    # Add global styling for the entire website
    st.markdown("""
        <style>
        /* Set background color for the entire page */
        body {
            background-color: #f7f8fa; /* Light, neutral background */
            color: #2c3e50; /* Text color for better readability */
            font-family: 'Arial', sans-serif;
        }

        /* Style the main title */
        .main-title {
            font-family: 'Arial', sans-serif;
            font-size: 50px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        /* Style the subtitle */
        .sub-title {
            font-family: 'Arial', sans-serif;
            font-size: 24px;
            margin-top: 0;
            margin-bottom: 30px;
        }

        /* Style expanders */
        .st-expander {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background: #ffffff; /* White background for expanders */
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
        }

        /* Style buttons */
        .stButton > button {
            background-color: #6c5ce7; /* Button background */
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            transition: 0.3s ease;
            cursor: pointer;
        }

        /* Hover effect for buttons */
        .stButton > button:hover {
            background-color: #00cec9; /* Hover color */
        }
        </style>
    """, unsafe_allow_html=True)

    # Fancy title and subtitle
    st.markdown("<h1 class='main-title'>Introduction</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Interactive Data Exploration Tool</p>", unsafe_allow_html=True)

    # Project overview section
    st.write("An Interactive Data Exploration Tool for Obesity Rates, Income, and Pharmaceutical Stock Sales.")
    st.write("Explore insights and correlations between health, economics, and industry trends using this tool.")

    # File paths 
    bmi_data_path = "./data/CleanCDC_2.csv"
    income_data_path = "./data/FRED.csv"
    stock_data_path = "./data/stock.csv"
    
    # Load datasets
    try:
        bmi_data = pd.read_csv(bmi_data_path)
        income_data = pd.read_csv(income_data_path)
        stock_data = pd.read_csv(stock_data_path)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
        return

    # Display datasets with expanders
    st.write("### Datasets Display")

    with st.expander("📊 Data 1: BMI Data from CDC"):
        st.dataframe(bmi_data.head(10))

    with st.expander("💰 Data 2: Median Household Income Data"):
        st.dataframe(income_data.head(10))

    with st.expander("📈 Data 3: Pharmaceutical Stock Data"):
        st.dataframe(stock_data.head(10))

    # Team members section
    st.write("### Team Members")
    st.markdown("""
    <p style="font-size: 18px;">
        1) HaYoung (Clara) Son &emsp;&emsp; 2) Ching (Jing) Chuang &emsp;&emsp; 3) Hyuntae Roh
    </p>
    """, unsafe_allow_html=True)


from NLP.main import handle_user_input  # handle_user_input is a gateway function between Streamlit and Demo(for db exploration, example query, data retrieval)

#----------------------------------------------------------------------------------------------
# Streamlit interaction
def page2():
    st.title("ChatDB: Chatbot Interface")
    st.write("Welcome to ChatDB! This is your Database query assistant. You can choose DB among MySQL and Firebase.")

    def session_initialization():
        # Initialize chat history and context in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []  # Stores chat history
        if "stage" not in st.session_state:
            st.session_state.stage = "initial"  # Tracks the current stage of the interaction
        if "user_input_nlq" not in st.session_state:
            st.session_state.user_input_nlq = None  # Stores user's choice of NLQ option
        if "user_input_db" not in st.session_state:
            st.session_state.user_input_db = None  # Stores user's database choice
        if "user_input_printout" not in st.session_state: 
            st.session_state.user_input_printout =None #Stores user's retrieval print-out choice
        if 'response' not in st.session_state:
            st.session_state.response = None
        if 'user_input' not in st.session_state:
            st.session_state.user_input = None 
        if 'retrieved_data' not in st.session_state: 
            st.session_state.retrieved_data =None 

    session_initialization() 

    # Welcoming message from the assistant
    if st.session_state.stage == 'initial' and len(st.session_state.messages)==0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm ChatDB_39, your assistant. How can I help you today? Please choose an option: 1 (Database) 2 (Examples), 3 (NLQ)."
        })

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Input box for user interaction
    if user_input := st.chat_input("Type your message here..."):
        # Append user's message to chat history
        user_input = user_input.strip() 
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Matches
        match_enter_query = pattern_match('example query|explore|describe|display|show|list|identify|retrieve|tell|select|get', user_input) # direct path to go to stage=='enter_query'
        match_initial_quiery = pattern_match('initial|initialize|redo', user_input) # direct path to go to stage=='initial' 
        match_nlq = pattern_match('nlq', user_input) # direct path to go to stage == 'choose_retrieve_option' for NLQ input 
        match_sql = pattern_match(pattern='1|sql|mysql', user_input= user_input)
        match_fire = pattern_match(pattern='2|fire|firebase', user_input= user_input) 
        match_explore = pattern_match(pattern='1|database|db|db exploration|explore db',user_input=user_input)
        match_retrieve = pattern_match(pattern='2|examples|example|see example|see example query',user_input=user_input)

        # Process user's input based on the current stage
        #-- 1. initial stage
        if st.session_state.stage == "initial" or match_initial_quiery: 
            st.session_state.response = None 
            st.session_state.retrieved_data = None 
            if user_input not in ['1','database','db','2','examples','example','3','nlq','initial','initialize','redo']:
                st.session_state.response = "I didn't understand. Please choose an option: 1 (DB Exploration) 2 (See Example query), 3 (NLQ)."
            else: 
                st.session_state.user_input_nlq = user_input
                if match_initial_quiery:
                    st.session_state.stage = 'closing'

#                elif match_nlq: 
#                    st.session_state.stage = 'choose_retrieve_option' 
#                    response= "Jump to the choose_retrieve_option stage"
#                    assistant_response(response)
                
                else:
                    st.session_state.stage = "choose_db"
                    response = "Which DB do you want? Input the number or name: 1. MySQL / 2.Firebase"     
                    assistant_response(response)           
        
        #-- 2.a1. DB selection stage
        elif st.session_state.stage == "choose_db":
            if match_sql : 
                st.session_state.user_input_db = "mysql"

            elif match_fire :
                st.session_state.user_input_db = "firebase"

            if match_explore:
                st.session_state.stage = 'choose_retrieve_option'
                response = "You've selected MySQL. Do you want to check the overview about databse?"
                assistant_response(response)

            elif match_retrieve:
                st.session_state.stage = "choose_retrieve_option"
                response = "Would you like to retrieve the actual data from DB and print them out?"
                assistant_response(response)

            else:
                response = "Invalid database choice. Please choose either MySQL (1) or Firebase (2)."
                assistant_response(response)


        #-- 2.a2. DB exploration stage 
        elif st.session_state.stage == 'explore_db': 
            if user_input in ['y','yes','ok','okay'] :
                response = 'First, let me explain what table you can look in our SQL. Currently we have three datasets: CDC, FRED, and STOCK.'
                assistant_response(response)

                response = """ - CDC: 14 Attributes and 288 records.\n- FRED: 2 Attributes and 40 records.\n- STOCK: 3 Attributes and 454 records.\n(MySQL) To see the further information, hit 'explore {CDC | FRED | STOCK} attribute'\n(Firebase) To see the further information, hit 'explore {CDC | FRED | STOCK}'
                        """
                assistant_response(response)

                response = f"Alright! Please look up the command examples above. Tell me which table or attribute information do you want to see. Your current DB is {st.session_state.user_input_db}."
                assistant_response(response)

            st.session_state.stage = "enter_query"  # Reset the stage after processing the query            

        #-- 2.b1. Retrieval option setting stage
        elif st.session_state.stage == 'choose_retrieve_option' :
            if user_input.lower() in ['y','yes','ok']:
                st.session_state.user_input_printout = True
                st.session_state.stage = "enter_query"
            else: 
                st.session_state.user_input_printout = False 

            if st.session_state.user_input_db == 'mysql':
                response = "Please refer to available commands: "
                assistant_response(response)
                response = """(Explore DB) explore {CDC | FRED | STOCK} {attribute}' \n(View example query) example query {where|groupby|orderby|having|aggregation}. """
                assistant_response(response)
            else: 
                response = "Please refer to available command: " 
                assistant_response(response)
                response = """(Explore DB) explore {CDC | FRED | STOCK}' \n(View example query) example query {where|groupby|orderby|having|aggregation}. """
                assistant_response(response)

        #-- 2.b2. Query request stage

        elif st.session_state.stage == 'enter_query' or match_enter_query: 
            user_input_nlq = st.session_state.user_input_nlq
            user_input_db = st.session_state.user_input_db
            user_input_printout = st.session_state.user_input_printout 
            st.session_state.response, st.session_state.retrieved_data = handle_user_input(
                    user_input_nlq, 
                    user_input_DB=user_input_db, 
                    user_query=user_input, 
                    print_out=user_input_printout
                )
            st.session_state.stage = 'stand_by'

        ############################################################################
        # Print out assisntant's response: 
        ## Streaming effect for assistant's response
        if st.session_state.stage is not 'closing' and st.session_state.response is not None:
            assistant_response(st.session_state.response)
        if st.session_state.retrieved_data is not None and st.session_state.stage is not 'closing':
            assistant_response(st.session_state.retrieved_data)
        ############################################################################

        #-- 3. Stand-by stage
        if st.session_state.stage == "stand_by":
            st.session_state.response = None  
            st.session_state.stage = 'closing' 
            response = "Anything else I can help you with? If you want to go back to the first stage to change your current stage, enter 'initial'. If you want to switch the database, hit 'switch'. If you want to keep looking examples, 'example query {where|having|...etc}' or 'example query {GET|range|orderBy|...etc}' "
            assistant_response(response)
            

        #if user_input in ['initial','initialize','switch']: 
        #-- 4. Closing stage
        elif st.session_state.stage == "closing" or match_initial_quiery:
            match = pattern_match('initial|switch|example|explore|display|show|list|identify|retrieve|tell|select|get', user_input) 
            #match2 = pattern_match('|display|show|list|identify|retrieve|tell|select|get',user_input) 
            if match : 
                response  = "Please wait a moment... all set! Hit Enter to proceed."
                assistant_response(response)

                if 'initial' in match.group():
                    st.session_state.stage = "initial"
                    st.session_state.user_input = "initial" 
                    # initialize session_state: 
                    st.session_state.response = None 
                    st.session_state.retrieved_data = None 
                    response = "Hello! I'm ChatDB_39, your assistant. How can I help you today? Please choose an option: 1 (Database) 2 (Examples), 3 (NLQ)."
                    assistant_response(response) 

                elif 'switch' in match.group(): 
                    st.session_state.stage = "enter_query"
                    # initialize session_state:
                    st.session_state.response = None 
                    st.session_state.retrieved_data = None 
                    st.session_state.user_input_db = 'mysql' if st.session_state.user_input_db is 'firebase' else 'firebase' 
                    st.session_state.user_input = None 
                    response = f"Your DB has been switched. Current DB: {st.session_state.user_input_db}"
                    assistant_response(response) 
                    response = "Know you can intput your specific query."
                    assistant_response(response) 

                else: 
                    st.session_state.stage = 'enter_query'
                    #response = "Hit 'go' to proceed."
                    #assistant_response(response)  
    
            else: 
                st.session_state.stage = "stand_by"
                response = "Unvalid query. Please refer to : { initial | switch | example query ~ }"
                assistant_response(response) 
                



def assistant_response(response):
        assistant_message_container = st.chat_message("assistant")
        with assistant_message_container:
            full_response, is_code = stream_effect(response) #-- Gives streaming effect on the assitant's response 

        # Append the full assistant's response to chat history
        append_response_to_chat(full_response, is_code) 

def stream_effect(response): 
    if response is None:
        response_placeholder = st.empty()
        response_placeholder.markdown("No response to display.")
        return "", False

    # Decode bytes to string if necessary
    if isinstance(response, bytes):
        response = response.decode("utf-8")  # Decode using UTF-8

    # Convert tuple to a string if needed
    if isinstance(response, tuple):
        response = "\n".join([str(item) for item in response])

    # Convert list or tuple to a string if needed
    if isinstance(response, (list, tuple)):
        # Handle lists of rows (e.g., SQL query results)
        if isinstance(response[0], (list, tuple)):  # List of rows
            response = "\n".join(["  ".join(map(str, row)) for row in response])
        else:  # Flat list or tuple
            response = "\n".join(map(str, response))

    response_placeholder = st.empty()
    full_response = response  # Full response text
    displayed_text = ""
    is_code = False 

    # Check if the response is tabular (contains multiple lines)
    if "\n" in full_response:  # Likely a tabular result
        lines = full_response.split("\n")
        for line in lines:
            displayed_text += line + "\n"
            response_placeholder.markdown(f"```\n{displayed_text}\n```")  # Render as a code block
            time.sleep(0.1)
        is_code = True 
    else:
        # Stream the response word by word for normal text
        for word in full_response.split():
            displayed_text += word + " "
            response_placeholder.markdown(displayed_text)
            time.sleep(0.1)

    return full_response, is_code 

def append_response_to_chat(full_response, is_code=False):
    """
    Append response to chat history with optional code formatting.
    """
    if is_code:
        full_response = f"```\n{full_response}\n```"  # Wrap response in triple backticks
    st.session_state.messages.append({"role": "assistant", "content": full_response})


def pattern_match(pattern, user_input):
    # Add word boundaries around the pattern
    bounded_pattern = fr'\b(?:{pattern})\b'
    match = re.search(bounded_pattern, user_input, re.IGNORECASE)
    return match 

#------------------------------------------------------------------------------------------
# Page 3: Data Analysis
def page3():
    st.title("Data Analysis")
    st.write("Welcome to the Data Analysis page! Here, you can explore insights and visualize the relationships between BMI, income, and pharmaceutical stock data.")

    # Obesity vs Pharmaceutical Stocks Correlational Analysis 
    st.subheader("Obesity vs Pharmaceutical Stocks")
    st.write("Below is a series of correlational analyses comparing different obesity levels with pharmaceutical stock data.")

    # Display images in a 2x2 grid 
    col1, col2 = st.columns(2)
    with col1:
        st.image("./images/normal_vs_stocks.png", caption="Normal vs. Stock Data")
        st.image("./images/obesity_2_vs_stocks.png", caption="Obesity Level 2 vs. Stock Data")
    with col2:
        st.image("./images/obesity_1_vs_stocks.png", caption="Obesity Level 1 vs. Stock Data")
        st.image("./images/obesity_3_vs_stocks.png", caption="Obesity Level 3 vs. Stock Data")

    st.markdown("""
    * Positive Correlation with Obesity: 
     \n Both NVO and LLY show increasing stock values as obesity levels rise, with stronger correlations for higher obesity categories (e.g., Obesity_3). NVO consistently exhibits a stronger correlation compared to LLY, indicating its stock performance is more closely tied to obesity-related trends.
    * Negative Correlation with Normal Weight: 
     \n Both companies' stock values decrease as the proportion of individuals in the normal weight range increases, with NVO showing a stronger negative correlation than LLY.
    """)

    # Additional Correlation Analysis Image
    st.subheader("Obesity vs Median Income")
    st.write("Below is a correlational analyses comparing different obesity levels with median household income.")
    st.image("./images/fred_all_correlation_final.png")
    st.markdown("""

    * Normal (r = -0.7359): 
    \n A strong negative correlation indicates that as income increases, the proportion of normal-weight individuals decreases.
    
    * Obesity_1 to Obesity_3 (r = 0.6875 to 0.7192): 
    \n Positive correlations suggest that higher incomes are associated with greater proportions of individuals in higher obesity categories, with the strongest correlation in Obesity_2.
    """)

# Main Function: Navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Introduction", "💬 ChatDB", "📊 Analytics"]
    )

    if page == "🏠 Introduction":
        page1()  # Your existing Introduction page function
    elif page == "💬 ChatDB":
        page2()  # Updated ChatDB page
    elif page == "📊 Analytics":
        page3()  # Your existing Analytics page function

# Run the app
if __name__ == "__main__":
    main()
