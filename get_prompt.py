from tavily import TavilyClient
import streamlit as st
import json
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mattshumer/Reflection-Llama-3.1-70B")

tavily_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

def get_bot_instructions():
    instructions = ""
    with open("bot_instructions.txt" , "r") as file:
        instructions = file.read()

    return instructions

def get_cfr_search_results(user_input) -> str:

    search_results = tavily_client.search(query=user_input ,
                                          search_depth="advanced" ,
                                          max_results=25 ,
                                          include_domains=["ecfr.gov"],
                                          include_answer=True,
                                          include_raw_content=False, )
    
    print("CFR Search Results" , search_results)

    return json.dumps(search_results)

def get_fda_search_results(user_input)->str:

    search_results = tavily_client.search(query=user_input ,
                                          search_depth="advanced" ,
                                          max_results=25 ,
                                          include_domains=["fda.gov"],
                                          exclude_domains=["usda.gov"],
                                          include_answer=True,
                                          include_raw_content=False)
    
    
    print("FDA Search Results" , search_results)
    return json.dumps(search_results)

def get_token_count(prompt :str)->int:

    return len(tokenizer(prompt)["input_ids"])


def get_prompt(user_input : str , use_cfr : bool = True , use_fda : bool = True):

    if(user_input==""):
        raise "The user must give some input"
    
    bot_instructions = get_bot_instructions()

    cfr_search_results = get_cfr_search_results(user_input=user_input) if use_cfr else ""

    fda_search_results = get_fda_search_results(user_input) if use_fda else ""

    prompt= f'SYSTEM INSTRUCTIONS : {bot_instructions}\n\nCFR SEARCH RESULTS : {cfr_search_results}\n\nFDA SEARCH RESULTS : {fda_search_results}\n\nUSER INPUT:{user_input}'


    token_count = get_token_count(prompt)
    print(token_count)
    if token_count < 128_000:
        return prompt
    else:
        return user_input
    
    
    
