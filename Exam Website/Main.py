# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:01:23 2022

@author: Lenovo
"""

import streamlit as st
import pyrebase
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import pyttsx3



def countdown(deadline_time, timer_name, intro_msg, outro_msg = ''):
    pyttsx3.speak(intro_msg)
    with st.empty():
        while(True):
            now = datetime.now()
            if(deadline_time > now):
                st.metric(timer_name, str(deadline_time - now).split(".")[0])
                time.sleep(1)
            else:
                break
        
    pyttsx3.speak(outro_msg)
    
    
    
def submit_exam():
    for qid in st.session_state.saq_q_id:
        answer = {
            "exam_id" : st.session_state.examination_id,
            "sub_question_id" : qid,
            "student_id" : st.session_state.stud_id,
            "answer" : st.session_state[qid],
            "correct_keywords" : "",
            "reference_keywords" : "",
            "missing_keywords" : "",
            "score" : 0,
            "verified" : 0
        }
        
        stud_info = {
            "student_id" : st.session_state.stud_id,
            "student_email" : st.session_state.stud_id + "@kdu-online.com",
            "student_name" : st.session_state.stud_name
        }
    
        st.session_state.db.child("student_answers").push(answer)
        st.session_state.db.child("student_information").child(st.session_state.stud_id).set(stud_info)
    
    st.success('All Answers submitted.')
    pyttsx3.speak("Examination submission confirmed. Thank you for taking the examination.")
    

def display_questions():
    
    line = '''
    ---
    '''

    exam = st.session_state.db.child("exams").order_by_child("exam_id").equal_to(st.session_state.exam_id).get()
    
    qid = ''
    exam_title = ''
    start_time_ = ''
    duration = 0
    # Loading question information
    for e in exam.each():
        qid = e.val()['questions']
        exam_title = e.val()['exam_title']
        start_time_ = e.val()['date'] + ' ' + e.val()['start_time'] 
        duration = e.val()['duration_minutes']
                
    q_num = 0
    question_number = []
    question_description = []
    total_marks = []
    num_of_subques = []
    subques = []
    for q_id in qid:
        q_num += 1
        question = st.session_state.db.child('questions').order_by_child('question_id').equal_to(q_id).get()
    
        for q in question.each():
            question_number.append(q_num)
            question_description.append(q.val()['question_description'])
            total_marks.append(q.val()['total_marks'])
            num_of_subques.append(q.val()['num_of_subques'])
            subques.append(q.val()['sub_questions'])
            if q.val()['total_marks'] > 1:
                m = "marks"
            else:
                m = "mark"
        
    
        
            
    questions = pd.DataFrame({'question_id': qid, 
                              'question_number': question_number, 
                              'question_description': question_description, 
                              'num_of_subques': num_of_subques, 
                              'total_marks': total_marks,
                              'm' : m})
    
    questions.sort_values(by=["question_number"], inplace = True)

    if 'start' not in st.session_state:
        st.session_state.start = False
        
    if 'end' not in st.session_state:
        st.session_state.end = False

    st.header(exam_title)
    col1, col2, col3 = st.columns(3)
    with col1:
        start_time = datetime.strptime(start_time_, '%Y-%m-%d %H:%M:%S')
        with st.spinner('Exam will begin soon...'):
            #st.snow()
            countdown(start_time, "Exam Starting In:", "Please wait until the examination starts.")
        st.session_state.start = True
        
    if st.session_state.start:
        exam_form = st.form('exam_form')
        with exam_form:
            for index, row in questions.iterrows():
                
                saq = st.session_state.db.child("saq_sub_questions").order_by_child("sub_question_number").order_by_child("question_id").equal_to(row['question_id']).get()
        
                
                st.markdown('**Question ' + str(index + 1) + '**')
                if row['num_of_subques'] > 0:
                    if row['total_marks'] > 1:
                        ques = row['question_description'] + " (" + str(row['total_marks']) +" marks)"
                    else:
                        ques = row['question_description'] + " (" + str(row['total_marks']) +" mark)"
                    st.write(ques)
                
                if 'saq_q_id' not in st.session_state:
                    st.session_state.saq_q_id = []
                
                for s in saq.each():
                    saq_question_num = "(" + chr(s.val()['sub_question_number'] + 96) + ") "
                    saq_question_id = s.val()['sub_question_id']
                    saq_description = s.val()['sub_question_description']
                    saq_marks = s.val()['marks']
            
                    if row['num_of_subques'] == 0:
                        if row['total_marks'] > 1:
                            ques = row['question_description'] + " (" + str(row['total_marks']) +" marks)"
                        else:
                            ques = row['question_description'] + " (" + str(row['total_marks']) +" mark)"
                        st.write(ques)
                        st.text_area(label = '', value = saq_question_id, key=saq_question_id)
                    else:
                        if saq_marks > 1:
                            ques = saq_question_num + saq_description + " (" + str(saq_marks) +" marks)"
                        else:
                            ques = saq_question_num + saq_description + " (" + str(saq_marks) +" mark)"
                        st.write(ques)
                        st.text_area(label = '', value = saq_question_id, key=saq_question_id)
                    
                    st.session_state.saq_q_id.append(saq_question_id)
                
                st.markdown('\n\n')
                st.markdown(line)
        
                
        
            btn_submit = st.form_submit_button('Submit Exam', on_click=submit_exam)
        
    with col2:
        end_time = datetime.strptime(start_time_, '%Y-%m-%d %H:%M:%S') + timedelta(minutes = duration)
        countdown(end_time, "Exam Time Left:", "You may begin the exam.")
        st.session_state.end = True

    with col3:
        end_time = datetime.strptime(start_time_, '%Y-%m-%d %H:%M:%S') + timedelta(minutes = duration + 2)
        #countdown(start_time, "Force Submitting In:", "Time's up! Please tidy-up your answers. Force submit will occur in one minute time.", "Thank you for taking the examination. Have a nice day ahead!")
        countdown(start_time, "Buffer Time:", "Time's up! Please tidy-up your answers and submit within the buffer time!", "The examination has ended. Thank you for taking the examination. Have a nice day ahead!")

    
        
def verify_exam_login():
    if not st.session_state.student_id:
        st.error('Please Fill Up Your Student ID!')
    elif not st.session_state.student_name:
        st.error('Please Fill Up Your Student Name!')
    elif not st.session_state.exam_id:
        st.error('Please Fill Up the Exam ID!')
    elif not st.session_state.password:
        st.error('Please Fill Up the Exam Password!')
    else:
        if st.session_state.db.child('exams').child(st.session_state.exam_id).shallow().get().val():    
            exam = st.session_state.db.child("exams").order_by_child("exam_id").equal_to(st.session_state.exam_id).get()
            
            if 'stud_id' not in st.session_state:
                st.session_state.stud_id = st.session_state.student_id
                
            if 'stud_name' not in st.session_state:
                st.session_state.stud_name = st.session_state.student_name
                
            if 'examination_id' not in st.session_state:
                st.session_state.examination_id = st.session_state.exam_id
                
             
            pw = ''
            for e in exam:
                pw = e.val()['exam_password']
            
            if st.session_state.password == pw:
                st.session_state.login = True
                st.write("")
                    
                display_questions()
                
            else:
                st.error('Incorrect Password!')
        else:
            st.error("Incorrect Exam Id!")


def login_form():
    st.header('Exam Login')
    with st.form('login_exam'):
        st.text_input('Student ID: ', key='student_id')
        st.text_input('Student Name: ', key='student_name')
        st.text_input('Exam ID: ', key='exam_id')
        st.text_input('Exam Password: ', key='password')
        submit = st.form_submit_button('Submit', on_click=verify_exam_login)





# Firebase configuration
if 'config' not in st.session_state:
    # Firebase configurations
    st.session_state.config = {
        "apiKey": "AIzaSyB_kmIlFKKHu8HVPZEdFh1tiTQmX9lVOKg",
        "authDomain": "automated-exam-marking-system.firebaseapp.com",
        "databaseURL": "https://automated-exam-marking-system-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "automated-exam-marking-system",
        "storageBucket": "automated-exam-marking-system.appspot.com",
        "messagingSenderId": "1097146013231",
        "appId": "1:1097146013231:web:c349e46afaa63957f4d8da",
        "measurementId": "G-RS9RM4LKC1"
    } 
    
if 'firebase' not in st.session_state:
    st.session_state.firebase = pyrebase.initialize_app(st.session_state.config)

if 'db' not in st.session_state:
    st.session_state.db = st.session_state.firebase.database()

if 'login' not in st.session_state:
    st.session_state.login = False
    

    
if not st.session_state.login:
    login_form()