import streamlit as st
import pandas as pd
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


def page2():
    st.title("ChatDB: Chatbot Interface")
    st.write("Welcome to ChatDB! This is your chatbot interface.")

    # Initialize chat history with a guideline message
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Guidelines in an expandable box
    with st.expander("📜 Guidelines"):
        st.markdown("""
        Welcome to the ChatDB chatbot interface! Here are some guidelines to help you get started:

        - **Be specific and concise** when asking questions.
        - **Include relevant context** for more accurate responses.
        - **Avoid overly vague or broad queries.**

        Feel free to start exploring your data with queries!
        """)

    # Display chat history from session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    if user_input := st.chat_input("Type your message here..."):
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Simulate assistant response with streaming effect
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = f"You said: {user_input}"  # Replace with actual processing logic
            response = ""
            for word in full_response.split():
                response += word + " "
                response_placeholder.markdown(response)
                time.sleep(0.1)

        # Append assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})








# Page 3: Data Analysis
def page3():
    st.title("Data Analysis")
    st.write("Welcome to the Data Analysis page! Here, you can explore insights and visualize the relationships between BMI, income, and pharmaceutical stock data.")

    # Obesity vs Pharmaceutical Stocks Correlational Analysis 
    st.subheader("Obesity vs Pharmaceutical Stocks")
    st.write("Below is a series of analyses comparing different obesity levels with pharmaceutical stock data.")

    # Display images in a 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        st.image("/Users/clarason/Downloads/normal_vs_stocks.png", caption="Normal vs. Stock Data")
        st.image("/Users/clarason/Downloads/obesity_2_vs_stocks.png", caption="Obesity Level 2 vs. Stock Data")
    with col2:
        st.image("/Users/clarason/Downloads/obesity_1_vs_stocks.png", caption="Obesity Level 1 vs. Stock Data")
        st.image("/Users/clarason/Downloads/obesity_3_vs_stocks.png", caption="Obesity Level 3 vs. Stock Data")

    st.markdown("""
    **Interpretation:**
    Fixxx
    """)

    # Additional Correlation Analysis Image
    st.subheader("Obesity vs Median Income")
    st.image("/Users/clarason/Downloads/fred_all_correlation_final.png")
    st.markdown("""
    **Interpretation:**
    Fixxx
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
