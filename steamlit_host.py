# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:02:18 2022
@author: Connor
"""

import streamlit as st
from streamlit_chat import message
import requests
import time

st.set_page_config(
    page_title="WiseBot",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/Buddha/BrightBot-med"
headers = {"Authorization": 'Bearer {}'.format(st.secrets['api_key'])}

st.header("WiseBot")
#st.markdown("[Github](https://github.com/---)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = [' ']

if 'past' not in st.session_state:
    st.session_state['past'] = [' ']
    
for i in range(len(st.session_state['generated'])-1):
    message(st.session_state["generated"][i], key=str(i))
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ")
    return input_text 


user_input = get_text()

if user_input and len(user_input)>0:
    payload = {
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },
        "parameters": {
            "temperature": 16.0,
            "repetition_penalty": 1.33
            },
        # "options": {
        #     "wait_for_model": True,
        #     },
    }
    bot_response = None
    while not bot_response:
        response = query(payload)
        bot_response = response.get('generated_text', None)
        
        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if response['error'] == 'Model Buddha/BrightBot-med is currently loading':
                time.sleep(15)


    st.session_state.past.append(user_input)
    st.session_state.generated.append(response["generated_text"])
    # max_context = 4
    # if len(st.session_state.past) > max_context:
    #     st.session_state['past'] = st.session_state.past[-max_context:]
    # if len(st.session_state.generated) > max_context:
    #     st.session_state['generated'] = st.session_state.generated[-max_context:]
        