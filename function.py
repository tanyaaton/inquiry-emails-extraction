import os
import logging, datetime
import pandas as pd

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompt import response_format_json, response_format_df

# now = datetime.datetime.now()
# formatted_datetime = now.strftime("%d-%m-%Y_%H%M")
# logging.basicConfig(filename=f'log/app_{formatted_datetime}.log', 
#                     level=logging.INFO, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
OPENAI_API_KEY=  os.getenv("OPENAI_API_KEY")

@st.cache_resource
def connect_openai_llm():
    client = OpenAI()
    return client


def generate_answer(openai_client, prompt):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages= prompt
    )
    response = completion.choices[0].message.content
    return response_format_df(response)


def create_dataframe(col_name,response_list):
    col = ["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]
    df = pd.DataFrame(index=col)
    df[col_name]=response_list
    return df

def display_dataframe(col_name,response_list):
    df_dis = create_dataframe(col_name,response_list)
    st.dataframe(df_dis, width=1000)