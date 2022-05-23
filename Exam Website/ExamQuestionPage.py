# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:07:53 2022

@author: Lenovo
"""

import streamlit as st
import pyrebase
import pandas as pd

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

line = '''
---
'''

exam_title_1 = 'Introduction to Data Science Quiz'
exam_title_2 = 'Knowledge Discovery & Data Mining'
exam_id = ''
num_of_ques = 0
exam = st.session_state.db.child("exams").order_by_child("exam_title").equal_to(exam_title_1).get()
student_id = '0127122'


for e in exam.each():
    exam_id = e.val()['exam_id']

question = st.session_state.db.child("questions").order_by_child("exam_id").equal_to(exam_id).get()

question_id = []
question_number = []
question_description = []
num_of_subques = []
total_marks = []
for q in question.each():
    question_id.append(q.val()['question_id'])
    question_number.append(q.val()['question_number'])
    question_description.append(q.val()['question_description'])
    num_of_subques.append(q.val()['num_of_subques'])
    total_marks.append(q.val()['total_marks'])
    
questions = pd.DataFrame({'question_id': question_id, 
                          'question_number': question_number, 
                          'question_description': question_description, 
                          'num_of_subques': num_of_subques, 
                          'total_marks': total_marks})

questions.sort_values(by=["question_number"], inplace = True)
    
with st.form('exam_form'):
    for index, row in questions.iterrows():
        
        saq = st.session_state.db.child("saq_sub_questions").order_by_child("sub_question_number").order_by_child("question_id").equal_to(row['question_id']).get()

        
        st.markdown('**Question ' + str(row['question_number']) + '**')
        if row['num_of_subques'] > 0:
            if row['total_marks'] > 1:
                ques = row['question_description'] + " (" + str(row['total_marks']) +" marks)"
            else:
                ques = row['question_description'] + " (" + str(row['total_marks']) +" mark)"
            st.write(ques)
        
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
                st.text_area(label = '', value = saq_question_id + student_id, key=saq_question_id + student_id)
            else:
                if saq_marks > 1:
                    ques = saq_question_num + saq_description + " (" + str(saq_marks) +" marks)"
                else:
                    ques = saq_question_num + saq_description + " (" + str(saq_marks) +" mark)"
                st.write(ques)
                st.text_area(label = '', value = saq_question_id + student_id, key=saq_question_id + student_id)
        
        
        st.markdown('\n\n')
        st.markdown(line)

        

    btn_submit = st.form_submit_button('Submit Exam')