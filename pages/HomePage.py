# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:27:45 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp
from PIL import Image
from datetime import datetime

class HomePage(HydraHeadApp): 
    def run(self):
        ##st.write(st.session_state.current_user)
        st.markdown("<h1 style='text-align: center; line-height: 120px;'>Automated Examination Marking System - Home Page</h1>", unsafe_allow_html=True)
        image = "https://raw.githubusercontent.com/junchao1507/FYP-Implementation/main/images/ComputerGrading.jpg"
        st.image(image, caption='', width=1450)
        
        if 'exam-title' not in st.session_state:
            st.session_state.exam_title = ''
            
        if 'date' not in st.session_state:
            st.session_state.date = ''
            
        if 'start_time' not in st.session_state:
            st.session_state.start_time = ''
            
        if 'duration_minutes' not in st.session_state:
            st.session_state.duration_minutes = 0
            
        if 'exam_pw' not in st.session_state:
            st.session_state.exam_pw = ''
            
        if 'num_of_ques' not in st.session_state:
            st.session_state.num_of_ques = 0
            
        if 'btn_submit_exam_info' not in st.session_state:
            st.session_state.btn_submit_exam_info = False
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("How to Use This System?")
            st.write("01. Create a new exam by filling up the form on your right.")
            st.write("02. Go to the 'Exam Dashboard page via the top navigation bar.")
            st.write("03. Go to the 'Exam Dashboard page via the top navigation bar.")
            st.write("04. Navigate yourself to the newly created exam via the left drop-down menu.")
            st.write("05. Start creating examination questions.")
            st.write("06. After you have completed the examination setup, you can send examination to your students via email.")
            st.write("07. After students have submitted their answers, go to the exam marking page to monitor the marking process.")
            st.write("08. Correct keywords will be highlighted and a score will be predicted. You may edit the score if you think it is inaccurate.")
            st.write("09. After the marking process has been completed, go to the exam analytics dashboard page to view exam analytics.")
            st.write("10. At the bottom of the exam analytics page, you may send examination results with feedback to your students via email")
                
        with col2:
            # Create examination form
            with st.form(key='create_exam_form'):
                st.header('**Create a New Exam**')
                st.session_state.exam_title = st.text_input(label='Exam Title: ')
                st.session_state.date = st.date_input('Start Date: ') 
                st.session_state.start_time = st.time_input('Start Time: ')
                st.session_state.duration_minutes = st.number_input('Duration in Minutes: ', min_value=0, value=0, step=1) 
                st.session_state.num_of_ques = st.number_input('Number of Questions: ', min_value=0, value=0, step=1) 
                st.session_state.exam_pw = st.text_input('Set a Password: ', type="password")
                st.session_state.btn_submit_exam_info = st.form_submit_button(label='Submit')
            
            
            if st.session_state.btn_submit_exam_info:
                # Ensure the user enters the exam title and exam password
                if not st.session_state.exam_title:
                    st.error("Please enter an exam title")
                elif not st.session_state.date:
                    st.error("Please do not leave the Date field blank. Use the default value if you have decided to update it later")
                elif not st.session_state.start_time:
                    st.error("Please do not leave the Start Time field blank. Use the default value if you have decided to update it later")
                elif not st.session_state.duration_minutes:
                    st.error("Please do not leave the Duration field blank. Use the default value if you have decided to update it later")
                elif not st.session_state.num_of_ques:
                    st.error("Please do not leave the Number of Questions field blank. Use the default value if you have decided to update it later")
                elif not st.session_state.exam_pw:
                    st.error("Please enter an exam password.")
                else:
                    # Save data into firebase real-time database
                    now = datetime.now()
                    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
                    e = {
                        'exam_password': st.session_state.exam_pw,
                        'exam_title': st.session_state.exam_title,
                        'questions' : "",
                        'num_of_ques': st.session_state.num_of_ques,
                        'duration_minutes': st.session_state.duration_minutes,
                        'date': str(st.session_state.date),
                        'start_time': str(st.session_state.start_time), 
                        'timestamp_created': timestamp,
                        # might be wrong
                        'user_id': st.session_state.current_user['user_id']
                        }
                    
                    ex = st.session_state.db.child('exams').push(e)
                    st.session_state.db.child("exams").child(ex['name']).update({"exam_id": ex['name']})
                    st.success('Exam Created Successfully.')    
        