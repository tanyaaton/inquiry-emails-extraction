import os
import logging, datetime
import pandas as pd

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


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
    return completion.choices[0].message.content


def create_hits_dataframe(hits, num_hits=10):
    if len(hits[0]) < 10:
        num_hits = len(hits[0])
    dict_display = {
        f'chunk{i}': [hits[0][i].text]
        for i in range(num_hits)
    }
    df = pd.DataFrame(dict_display).T
    df.columns = ['Reference from document']
    return df

def display_hits_dataframe(hits, num_hits=10, width=1000):
    df_dis = create_hits_dataframe(hits, num_hits)
    st.dataframe(df_dis, width=width)