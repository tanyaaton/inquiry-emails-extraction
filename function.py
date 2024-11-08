import os
import logging, datetime
import pandas as pd

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient


# from prompt import response_format_df

load_dotenv()
OPENAI_API_KEY=  os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

@st.cache_resource
def connect_openai_llm():
    client = OpenAI()
    return client

@st.cache_resource
def connect_tavily():
    tavily_client = TavilyClient(api_key=tavily_api_key)
    return tavily_client


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def generate_answer(openai_client, prompt):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages= prompt
    )
    response = completion.choices[0].message.content
    logging.info(response)
    return response


def create_dataframe(df,col_name, response_list):
    entities = ["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]
    df = pd.DataFrame(index=entities)
    df[col_name]=response_list
    return df


