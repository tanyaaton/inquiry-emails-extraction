import json
import ast

entities = ["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]

# instruction_json = """You are a helpful, respectful assistant. You will receive an INSURANCE REQUEST EMAIL in the speficied subject and its content. From the email, please extract the following entity in to jason format provided below
# [{"Yacht Model": ""},{"Yacht Length": ""},{"Year of Manufacture":""}{"Current Value/Purchase Price":""},{"Current Location":""},{"Intended Cruising Area":""},{"Owner's Name":""},{"Owner's Contact Information":""},{"Owner's Boating Experience":""},{"Previous Insurance Claims":""},{"Additional Equipment":""},{"Current Insurance Coverage":""},{"Other":""}]"""

instruction_dataframe = f"""You are a helpful, respectful assistant. You will receive an INSURANCE REQUEST EMAIL in the specified subject and its content. From the email, please extract the following entities into a list with the order specified below:
["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]
If the information is not provide for the specific entities, that element of the list should be None. Return only in the string of list format that can be directly transfer into python list.
"""

# instruction_dic = """You are a helpful, respectful assistant. You will receive an INSURANCE REQUEST EMAIL in the speficied subject and its content. From the email, please extract the following entity in to python dictionary format provided below
# {"Yacht Model": "","Yacht Length": "","Year of Manufacture": "","Current Value/Purchase Price": "","Current Location": "","Intended Cruising Area": "","Owner's Name": "","Owner's Contact Information": "","Owner's Boating Experience": "","Previous Insurance Claims": ","Additional Equipment": "","Current Insurance Coverage": "","Other": ""}
# Answer in Dictionary format only. Do not provide any further explanation. If the information is not provide for the specific entities, that value of the key should be None.
# """

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
            "content": "{",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]

# def response_format_json(response):
#     response_json = response.replace('\n', '').replace('json', '').replace('```', '').replace('', '')
#     data = json.loads(response_json)
#     return data

# def response_format_dic(response):
#     response_json = response.replace('\n', '').replace('python', '').replace('```', '').replace('', '')
#     data = json.loads(response_json)
#     return data

def response_format_df(response):
    response_list = ast.literal_eval(response)
    return response_list

def search_web(email_dic, tavily_client):
    yatch_model = email_dic[0]
    message = f'Search for {entities[:3]} of the {yatch_model}'
    response = tavily_client.search(message)
    return [response['results'][0]['url'], response['results'][1]['url'], response['results'][2]['url']]



# instruction_search_dic = """given you a list of 3 internet link resources that contain the missing information for the given Yatch Model PYTHON DICTIONARY.
# Please search through the links to find the information for the missing value (None) in the given PYTHON DICTIONARY. If all the informtion is found in the first link, there is no need to look in to the second or third link. If not, continue the search on the second link, and so on. 
# Replace the None value in PYTHON DICTIONARY with new information and return only the Python Dictionary format below: 
# {"Yacht Model": "","Yacht Length": "","Year of Manufacture": "","Current Value/Purchase Price": "","Current Location": "","Intended Cruising Area": "","Owner's Name": "","Owner's Contact Information": "","Owner's Boating Experience": "","Previous Insurance Claims": ","Additional Equipment": "","Current Insurance Coverage": "","Other": ""}
# If you are unable to locate the missing information, simply return the Python dictionary with the values unchanged. Do not provide any further explanation
# """

instruction_search_df = """You will be given a RESOURCE LINK and a PYTHON YATCH LIST. 
PYTHON YATCH LIST is a list of Yatch information in a list containing the following information respectively:
["Yacht Model", "Yacht Length", "Year of Manufacture", "Current Value/Purchase Price", "Current Location", "Intended Cruising Area", "Owner's Name", "Owner's Contact Information", "Owner's Boating Experience", "Previous Insurance Claims", "Additional Equipment", "Current Insurance Coverage", "Other"]
RESOURCE LINK is a list of 3 internet links that contain the missing information for the given PYTHON YATCH LIST.

Please search through the links to find the information for the missing value (None) in the given PYTHON YATCH LIST. If all the informtion is found in the first link, there is no need to look in to the second or third link. If not, continue the search on the second link, and so on. 
Replace the None value in PYTHON YATCH LIST with new information and return only the Python List format. If you are unable to locate the missing information, simply return the Python list with the values unchanged. Do not provide any further explanation
Return result only in list format that can be directly transfer into python list.
"""

def generate_search_prompt(email_dic,link):
    messages = {
        "messages": [
            {
            "content": f"""{instruction_search_df}""",
            "role": "system"
            },
            {
            "content": f"""PYTHON DICTIONARY: {email_dic}
RESOURCE LINK: {link}""",
            "role": "user"
            },
            {
            "content": "",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]