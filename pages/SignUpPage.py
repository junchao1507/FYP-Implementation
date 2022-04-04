# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:34:59 2022

@author: Jun Chao
"""

# Importing packages
import streamlit as st
from datetime import datetime
from validate_email import validate_email
from hydralit import HydraHeadApp
from PIL import Image
# from firebase import firebase
# from pyrebase import pyrebase

# =============================================================================
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# =============================================================================


class SignUpPage(HydraHeadApp):   

    def run(self):
        st.markdown("<h1 style='text-align: center; line-height: 120px;'>Automated Exam Marking System  - Sign-Up Page</h1>", unsafe_allow_html=True)
        image = "https://raw.githubusercontent.com/junchao1507/FYP-Implementation/main/images/ComputerGrading4.jpg"
        st.image(image, caption='', width=1450)
        
        # Sign up form -> to prevent page refresh after one input
        with st.form(key='signup_form'):
            username = st.text_input('Username: ')
            email = st.text_input('Email: ') 
            password = st.text_input('Password: ', type="password")
            btn_signup = st.form_submit_button(label='Sign Up')
        
        
        if btn_signup:
            # Check if the required fields are empty
            if not username:
                st.error("Please enter a username.")
            elif not email:
                st.error("Please enter an email.")
            elif not password:
                st.error("Please enter a password.")
            elif len(password) < 6:
                st.error("Password must contain at least 6 characters.")
            else:
                # Get the current timestamp
                now = datetime.now()
                reg_date = now.strftime("%d/%m/%Y %H:%M:%S")
                # Check if the email has already been registered.
                exists = False
                if st.session_state.users.empty == True:
                     exists = False
                else:
                    exists = email in st.session_state.users.values
                # If no, then can register
                if not exists:
                    # Check if the email is valid
                    valid = validate_email(email)
                    if valid:
                        # Store user info into firebase authentication as well as firebase real time database
                        user = st.session_state.auth.create_user_with_email_and_password(email, password)
                        
                        u = {
                            'user_id': user['localId'],
                            'username': username,
                            'email': email,
                            'password': password,
                            'reg_date': reg_date,
                            'del_date': None
                            }
                        
                        st.session_state.db.child('users').child(user['localId']).set(u)
                        st.session_state.users= st.session_state.users.append(u, ignore_index=True)
                        st.success('Sign Up successful.')
                        
                    else:
                        st.error("Invalid email.")
                else:
                    st.error('Account already exists.')
                
        if st.button('Login'):
            self.set_access(0, None)
            self.do_redirect()
        

        