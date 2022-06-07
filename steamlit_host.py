# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:02:18 2022

@author: Connor
"""

import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="WiseBot",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/Buddha/BrightBot-med"
headers = {"Authorization": st.secrets['api_key']}

st.header("WiseBot")
#st.markdown("[Github](https://github.com/---)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },
        "parameters": {
            "temperature": 16.0,
            "repetition_penalty": 1.33
            },
        "options": {
            "wait_for_model": True,
            },
    })

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["generated_text"])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
