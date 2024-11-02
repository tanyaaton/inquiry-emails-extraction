import logging
import datetime
import os

#for UI
import streamlit as st
import pandas as pd

# for function
from function import (connect_openai_llm, generate_answer, display_dataframe)
from prompt import generate_prompt


#---------- settings ----------- #
model_id_llm='gpt-4o'
model_id_emb="text-embedding-3-large"

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
    st.markdown("### Display Options")
    for customer_name in st.session_state.customer_data.keys():
        st.session_state.customer_visibility[customer_name] = st.checkbox(
            f"Show {customer_name}", value=True
        )


#===========================================================================================

if customer_name := st.text_input("customer's name"):
    if customer_email := st.text_area("Input customer's email content:", height=300): 
        print('processing...')
        logging.info(customer_email)
        prompt = generate_prompt(customer_email)
        logging.info(prompt)
        response_list = generate_answer(model_llm,prompt)
        logging.info(response_list)

        # Store customer data in session state
        st.session_state.customer_data[customer_name] = response_list
        df_current = st.session_state.customer_data_df
        df_current[customer_name] = response_list
        st.session_state.customer_visibility[customer_name] = True  # Show newly added data
        st.session_state.customer_data_df = df_current
        st.dataframe(df_current, width=1000)

    # Display data for visible customers
# for name, data in st.session_state.customer_data.items():
#     if st.session_state.customer_visibility.get(name, False):
#         st.subheader(f"Data for {name}")
#         display_dataframe(name, data)
