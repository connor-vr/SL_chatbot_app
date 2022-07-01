# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:02:18 2022
@author: Connor
"""

import streamlit as st
from streamlit_chat import message
import requests
import time

API_URL = "https://api-inference.huggingface.co/models/Buddha/BrightBot-med"
headers = {"Authorization": 'Bearer {}'.format(st.secrets['api_key'])}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ")
    return input_text 


payload = {
    "inputs": {
        "past_user_inputs": [],
        "generated_responses": [],
        "text": "Hi.",
    },
    "parameters": {
        "temperature": 2.8,
        "repetition_penalty": 1.63
        }
    }

_ = query(payload)

st.set_page_config(
    page_title="WiseBot",
    page_icon=":robot:"
)


st.header("WiseBot")
#st.markdown("[Github](https://github.com/---)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []



user_input = get_text()

if user_input and len(user_input)>0:
    payload = {
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },
        "parameters": {
            "temperature": 2.8,
            "repetition_penalty": 1.63
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
    max_context = 4
    if len(st.session_state.past) > max_context:
        st.session_state['past'] = st.session_state.past[-max_context:]
    if len(st.session_state.generated) > max_context:
        st.session_state['generated'] = st.session_state.generated[-max_context:]
    
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
