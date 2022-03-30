# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 05:35:31 2021

@author: Jun Chao
"""

# Importing packages
import streamlit as st
import streamlit_authenticator as stauth
# import pyautogui

import pandas as pd
import numpy as np

from datetime import datetime
from validate_email import validate_email

import re
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')



class CurrentUser:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.email = None
        self.password = None
        
        
    def set_user(self, u):
        self.user_id = u['user_id']
        self.username = u['username']
        self.email = u['email']
        self.password = u['password']


    def get_user_id(self):
        return self.user_id
    
    
    def get_username(self):
        return self.username
    
    
    def get_email(self):
        return self.email

    
    def get_password(self):
        return self.password
# =============================================================================
#     def sign_up_account(self, users):
#         st.header('**Sign-Up**')
#         
#         # Sign up form -> to prevent page refresh after one input
#         with st.form(key='signup_form'):
#             username = st.text_input(label='Username: ')
#             email = st.text_input('Email: ') 
#             password = st.text_input('Password: ', type="password")
#             btn_signup = st.form_submit_button(label='Sign Up')
#         
#         
#         if btn_signup:
#             now = datetime.now()
#             reg_date = now.strftime("%d/%m/%Y %H:%M:%S")
#             if users.empty == True:
#                  user_id = 1
#                  exists = False
#             else:
#                 user_id = users.iloc[-1]['user_id'] + 1
#                 exists = email in self.email
#             if not exists:
#                 valid = validate_email(email)
#                 if valid:
#                     users= users.append({
#                         'user_id': user_id,
#                         'username': username,
#                         'email': email,
#                         'password': password,
#                         'reg_date': reg_date,
#                         'del_date': None}, 
#                         ignore_index=True)
#                     
#                     st.success('Sign Up successful.')
#                 else:
#                     st.error("Invalid email.")
#             else:
#                 st.error('Account already exists. Please login.')
#         return users
#             
#         
#     def login_account(self, user):
#         st.header('**Login**')
#         
#         # Login form -> to prevent page refresh after one input
#         with st.form(key='login_form'):
#             email = st.text_input('Email: ') 
#             password = st.text_input('Password: ', type="password")
#             btn_login = st.form_submit_button(label='Login')
#             
#         login = False
#         
#         if btn_login:
#             exists = (user['email'] == email).any()
#             if exists:
#                 valid_credentials = (len(user[(user['email'] == email) & (user['password'] == password)]) == 1)
#                 
#                 if valid_credentials:
#                     login = True
#                     
#                     index = user.index
#                     user_indices = index[(user['email'] == email) & (user['password'] == password)]
#                     index = user_indices.tolist()
#                     
#                     self.index = index[0]
#                     self.user_id = user['user_id'].iloc[self.index]
#                     self.username = user['username'].iloc[self.index]
#                     self.email = user['email'].iloc[self.index]
#                     self.password = user['password'].iloc[self.index]
#                     self.reg_date = user['reg_date'].iloc[self.index]
#                     self.del_date = user['del_date'].iloc[self.index]
#                     
#                     st.success('Login successfully')
#                     
#                 else:
#                     st.error('Incorrect email or password.')
#                     retry = st.selectbox('Do you want to continue?: ', ('Yes', 'No'))
#                     if retry == 'Yes':
#                         self.login_account()
#             else:
#                 st.error('Account not found.')
#         return login
# =============================================================================
        
        
# =============================================================================
#     def edit_account(self):
#         edit_menu = st.selectbox('Edit Account Details: ', ('Change Username', 'Change Email', 'Change Password'))
#         edit_menu = st.text_area('Enter Number (1-3): ')
#         login = self.login_account()
#         if login:
#             locate = (self.user['email'] == self.email) & (self.user["password"] == self.password)
#             if edit_menu == 'Change Username':
#                 username = st.text_area('Enter New Username: ')
#                 self.user.at[locate ,'username'] = username
#                 self.username = username
#                 st.write('Username updated.')
#             elif edit_menu == 'Change Email':
#                 email = st.text_area('Enter New Email: ')
#                 self.user.at[locate ,'email'] = email
#                 self.email = email
#                 st.write('Email updated.')
#             elif edit_menu == 'Change Password':
#                 password = st.text_area('Enter New Password: ')
#                 self.user.at[locate ,'password'] = password
#                 self.password = password
#                 st.write('Password updated.')
# =============================================================================
