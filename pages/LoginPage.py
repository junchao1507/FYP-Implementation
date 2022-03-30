# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:05:27 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp
from PIL import Image


class LoginPage(HydraHeadApp): 
    def run(self):
        st.markdown("<h1 style='text-align: center; line-height: 120px;'>Automated Exam Marking System  - Login Page</h1>", unsafe_allow_html=True)
        image = Image.open(r"C:\Users\Lenovo\OneDrive\Desktop\Y3S2\FYP\FYP-Implementation\images\ComputerGrading4.jpg")
        st.image(image, caption='', width=1450)
        
        # Login form -> to prevent page refresh after one input
        with st.form(key='login_form'):
            # Gets user input
            email = st.text_input('Email: ', autocomplete=('email')) 
            password = st.text_input('Password: ', type="password")
            btn_login = st.form_submit_button(label='Login')
            
        index = None
        
        if btn_login:
            # Check if the required fields are empty
            if not email:
                st.error("Please enter your email.")
            if not password:
                st.error("Please enter a password.")
                
            # Checks if the user exists
            exists = (st.session_state.users['email'] == email).any()
            
            # If user exists
            if exists:
                # Validates user's credentials
                valid_credentials = (len(st.session_state.users[(st.session_state.users['email'] == email) & 
                                                                (st.session_state.users['password'] == password)]) > 0)
                
                # If user's credentials is validated
                if valid_credentials:
                    # Login via firebase auth
                    # Set current user using dict and display success message
                    # Hydralit grant access to the user
                    # Redirects the user to the main pagr
                    st.session_state.auth.sign_in_with_email_and_password(email, password)
                    st.session_state.current_user = st.session_state.users[st.session_state.users['email'] == email].to_dict('records')[0]
                    st.success('Login successfully')
                    self.set_access(1, email)
                    self.do_redirect()
                    
                else:
                    # No access granted and display error message
                    self.session_state.allow_access = 0
                    self.session_state.current_user = None
                    st.error('Incorrect email or password.')
                    
            else:
                # Error message if the user does not exist.
                st.error('Account not found. Please sign-up.')

        
        if st.button('Sign Up'):
            self.set_access(-1, 'guest')
            self.do_redirect()
            
            