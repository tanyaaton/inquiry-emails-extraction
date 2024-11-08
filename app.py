import logging
import datetime
import os
import json

import streamlit as st
import pandas as pd

# function
from function import connect_openai_llm, connect_tavily, generate_answer, convert_df
from prompt import generate_prompt, search_web, generate_search_prompt, response_format_df


# settings
model_id_llm='gpt-4o'

# Most GENAI logs are at Debug level.
now = datetime.datetime.now()
formatted_datetime = now.strftime("%d-%m-%Y_%H%M")
logging.basicConfig(filename=f'log/app_{formatted_datetime}.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(
    page_title="Yacht Insurance Inquiry Emails",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.header("Insurance Inquiry Emails Extraction 📮")

model_llm = connect_openai_llm()
tavily_client = connect_tavily()


# Initialize session state for customer data and visibility
if "customer_data" not in st.session_state:
    st.session_state.customer_data = {}
    index = ["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", 
               "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", 
               "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", 
               "Current Insurance Coverage", "Other"]
    st.session_state.customer_data_df = pd.DataFrame(index=index)

if "customer_visibility" not in st.session_state:
    st.session_state.customer_visibility = {}


# Sidebar contents
with st.sidebar:
    st.title("🌷Welcome")
    st.markdown('''
    ### Model Information
    - LLM Model: `gpt-4o`
    ''')

    # Toggle visibility for each customer
    st.markdown('''
        ### Display Options
        - choose customer name to display the data''')

    for customer_name in st.session_state.customer_data.keys():
        st.session_state.customer_visibility[customer_name] = st.checkbox(
            f"{customer_name}", value=True
        )

if customer_name := st.text_input("customer's name"):
    if customer_email := st.text_area("Input customer's email content:", height=300): 
        print('processing...')
        logging.info(customer_email)
        prompt = generate_prompt(customer_email)
        logging.info(prompt)
        email_dic = generate_answer(model_llm,prompt)
        print('ppppppppp',email_dic)
        logging.info(email_dic)
        
        link = search_web(email_dic, tavily_client)
        prompt_fill_na = generate_search_prompt(email_dic,link)
        logging.info(prompt_fill_na)
        response_list = generate_answer(model_llm,prompt_fill_na)
        logging.info(response_list)
        if isinstance(response_list, list): pass
        else: response_list = response_format_df(response_list)

        # Store customer data in session state
        st.session_state.customer_data[customer_name] = response_list
        df_current = st.session_state.customer_data_df
        df_current[customer_name] = response_list
        st.session_state.customer_visibility[customer_name] = True  # Show newly added data
        st.session_state.customer_data_df = df_current

# Display data for visible customers
if st.session_state.customer_visibility != {}:
    name_visible = [key for key, value in st.session_state.customer_visibility.items() if value]
    df_display =st.session_state.customer_data_df 
    st.dataframe(df_display[name_visible], width=1000)

    csv = convert_df(df_display)
    st.download_button("Press to Download",csv,
    f"result_{formatted_datetime}.csv",
    "text/csv",
    key='download-csv'
    )
