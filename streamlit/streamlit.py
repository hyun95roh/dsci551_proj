import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="551 Project", page_icon="📚")

# Page 1: Introduction
def page1():
    st.title("Introduction")
    # Overview section
    st.write("### Project Overview")
    st.write(
        "An Interactive Data Exploration Tool for Obesity Rates, Income, "
        "and pharmaceutical stock sales."
    )


    # File paths
    bmi_data_path = "/Users/clarason/Downloads/CleanCDC_2.csv"
    income_data_path = "/Users/clarason/Downloads/FRED.csv"
    stock_data_path = "/Users/clarason/Downloads/stock.csv"

    # Load datasets
    try:
        bmi_data = pd.read_csv(bmi_data_path)
        income_data = pd.read_csv(income_data_path)
        stock_data = pd.read_csv(stock_data_path)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
        return

    # Display datasets with expanders
    with st.expander("Data 1 : Centers for BMI Data from Disease Control and Prevention Data (CDC)"):
        st.dataframe(bmi_data.head(10))

    with st.expander("Data 2 : Median Household Income Data from Federal Reserve Economic Data (FRED)"):
        st.dataframe(income_data.head(10))

    with st.expander("Data 3 : Eli Lilly and Novo Nordisk Stock Data"):
        st.dataframe(stock_data.head(10))

    st.write("### Team Members")
    st.write("(1)HaYoung Son  ", " ", "  (2)Ching (Jing) Chuang  ", " ", "  (3)Hyuntae Roh")

# Page 2: ChatDB - Chatbot Interface
def page2():
    st.title("ChatDB: Chatbot Interface")
    st.write("Welcome to ChatDB! This is your chatbot interface.")

    # Query Guidelines Section
    with st.expander("## Query Guidelines -- Click for Assistance!"):
        st.write(
            "This is the guideline to make an input query. "
            "Please do the following:"
        )

    # Chatbot conversation history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input box for user query
    user_input = st.text_input("Enter your query:")

    # Handle user input when button is clicked
    if st.button("Chat!"):
        if user_input:
            # Reverse the order of words in the user's input
            reversed_words = " ".join(user_input.split()[::-1])
            response = f"{reversed_words}"
            
            # Append the response to the chat history
            st.session_state.chat_history.append(response)
    
    # Display the chat history
    st.write("### Chat History:")
    for response in st.session_state.chat_history:
        st.write(response)

# Page 3: Data Analysis
def page3():
    st.title("Data Analysis")
    st.write("Welcome to Page 3! This is the content for Page 3.")

# Main Function: Navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", 
        ["🏠 Introduction", "💬 ChatDB", "📊 Analytics"]
    )

    if page == "🏠 Introduction":
        page1()  # Updated Introduction page
    elif page == "💬 ChatDB":
        page2()
    elif page == "📊 Analytics":
        page3()

# Run the app
if __name__ == "__main__":
    main()
