import json
import ast

# instruction_json = """You are a helpful, respectful assistant. You will receive an INSURANCE REQUEST EMAIL in the speficied subject and its content. From the email, please extract the following entity in to jason format provided below
# [{"Yacht Model": ""},{"Yacht Length": ""},{"Year of Manufacture":""}{"Current Value/Purchase Price":""},{"Current Location":""},{"Intended Cruising Area":""},{"Owner's Name":""},{"Owner's Contact Information":""},{"Owner's Boating Experience":""},{"Previous Insurance Claims":""},{"Additional Equipment":""},{"Current Insurance Coverage":""},{"Other":""}]"""

instruction_dataframe = """You are a helpful, respectful assistant. You will receive an INSURANCE REQUEST EMAIL in the specified subject and its content. From the email, please extract the following entities into a list with the order specified below:
["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]
"""

def generate_prompt(email):
    messages = {
        "messages": [
            {
            "content": instruction_dataframe,
            "role": "system"
            },
            {
            "content": f"""INSURANCE REQUEST EMAIL: {email}""",
            "role": "user"
            },
            {
            "content": "",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]

def response_format_json(response):
    response_json = response.replace('\n', '').replace('json', '').replace('```', '').replace('', '')
    data = json.loads(response_json)
    return data

def response_format_df(response):
    response_list = ast.literal_eval(response)
    return response_list

# Always answer as helpfully as possible, while being safe. 
# Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
# Please ensure that your responses are socially unbiased and positive in nature. 
# If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
