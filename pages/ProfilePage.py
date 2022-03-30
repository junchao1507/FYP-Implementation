# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:27:47 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp

class ProfilePage(HydraHeadApp): 
    def run(self):
        st.markdown("<h1 style='text-align: center; line-height: 120px;'>Profile Page</h1>", unsafe_allow_html=True)
        
        st.markdown('**User ID:** ' + st.session_state.current_user['user_id'])
        st.markdown('**Email:** ' + st.session_state.current_user['email'])
        
        option = st.selectbox('Select Information to Update', ('Update Username', 'Update Password'))
        
        if option == 'Update Username':
            with st.form(key='update_username'):
                st.markdown('**Update Username**')
    
                username = st.text_input('Username: ', value = st.session_state.current_user['username'])
                chk_confirm = st.checkbox("I agree to change my username")
                btn_change_username = st.form_submit_button('Submit')
                
            if chk_confirm and btn_change_username:
                update_dict = {'username': username}
                st.session_state.db.child("users").child(st.session_state.current_user['user_id']).update(update_dict)
                st.session_state.current_user.set_username(username)
                msg = 'Username Updated Successfully'
                st.success(msg)
                
        if option == 'Update Password':
            with st.form(key='update_password'):
                st.markdown('**Update Password**')
                current_password = st.text_input('Enter Current Password: ', type = 'password')
                new_password = st.text_input('Enter New assword: ', type = 'password')
                chk_confirm = st.checkbox("I agree to change my password")
                btn_change_username = st.form_submit_button('Submit')
                
            if chk_confirm and btn_change_username:
                if st.session_state.current_user.get_password() == current_password:
                    update_dict = {'password': new_password}
                    st.session_state.db.child("users").child(st.session_state.current_user['user_id']).update(update_dict)
                    st.session_state.current_user.set_username(username)
                    msg = 'Username Updated Successfully'
                    st.success(msg)
                else:
                    st.error("Incorrect Password!")