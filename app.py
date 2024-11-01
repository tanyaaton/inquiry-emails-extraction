import logging
import datetime
import os

#for UI
import streamlit as st

# for function
from function import (connect_openai_llm, generate_answer, display_hits_dataframe)
from prompt import generate_prompt, response_format_json


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

# Sidebar contents
with st.sidebar:
    st.title("🌷Welcome")
    st.markdown('''
    ### Model Information
    - LLM Model: `gpt-4o`
    ''')


#===========================================================================================


if customer_email := st.text_area(
    "Input customer's email:", height=300
): 
    print('processing...')
    logging.info(customer_email)
    prompt = generate_prompt(customer_email)
    logging.info(prompt)
    response = generate_answer(model_llm,prompt)
    logging.info(response)
    response_json = response_format_json(response)
    st.text_area(label="Model Response", value=response_json, height=300)
    # display_hits_dataframe(hits)
