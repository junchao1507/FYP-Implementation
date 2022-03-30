# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 07:00:17 2021

@author: Jun Chao

"""


# Importing packages
import streamlit as st
import hydralit as hy
from PIL import Image

import pandas as pd
import numpy as np

from datetime import datetime
from validate_email import validate_email

# =============================================================================
# import re
# import nltk
# from nltk import WordNetLemmatizer
# from nltk.corpus import stopwords
# from nltk.corpus import wordnet as wn
# from nltk.tokenize import word_tokenize, sent_tokenize
# lemmatizer = WordNetLemmatizer()
# stop_words = stopwords.words('english')
# =============================================================================

from pages.SignUpPage import  SignUpPage
from pages.LoginPage import  LoginPage
from pages.HomePage import HomePage
from pages.DashboardPage import  DashboardPage
from pages.ProfilePage import  ProfilePage
from pages.ExamMarkingPage import ExamMarkingPage
from pages.ExamDashboardPage import ExamDashboardPage
from User import CurrentUser
from Exam import *
import pyrebase


# Declaring dataframes & set session states
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
    
if "auth" not in st.session_state:
    st.session_state.auth = st.session_state.firebase.auth()
    
# Load data from firebase
if 'users_db' not in st.session_state:
    st.session_state.users_db = st.session_state.db.child("users").get()
    

# Users dataframe
if 'users' not in st.session_state:
    st.session_state.users = pd.DataFrame(columns = ['user_id', 'username', 'email', 'password', 'reg_date', 'del_date'])
    
# Exams dataframe
if 'exams' not in st.session_state:
    st.session_state.exams = pd.DataFrame(columns = ['exam_id', 'exam_password', 'exam_title', 'num_of_ques', 'questions', 'duration_minutes', 'start_time', 'timestamp_created', 'user_id'])


# Current user
if 'current_user' not in st.session_state:
    st.session_state.current_user = CurrentUser()





# Load data into dataframe
if st.session_state.users_db.val() is not None:
    for u in st.session_state.users_db.each():
        unique = None
        temp_users = pd.DataFrame(columns = ['user_id', 'username', 'email', 'password', 'reg_date', 'del_date'])
        if st.session_state.users.empty == True:
            unique = u.val()
        else:
            temp_users = temp_users.append(u.val(), ignore_index = True)
            unique = temp_users[~temp_users["user_id"].isin(st.session_state.users["user_id"])]
        if len(unique) > 0:
            st.session_state.users = st.session_state.users.append(unique, ignore_index=True)
        
    

app = hy.HydraApp(title='Automated Examination Marking System')

app.add_app('Home', app=HomePage(),icon="🏠",is_home=True)
app.add_app('Sign Up', app=SignUpPage(), is_login=True, is_unsecure=True)
app.add_app('Login', app= LoginPage(), is_login=True)
app.add_app('Create Exam Questions',icon="📝", app=ExamDashboardPage())
app.add_app('Exam Marking',icon="✍️", app=ExamMarkingPage())
app.add_app('Exam Analytics Dashboard',icon="📊", app=DashboardPage())
app.add_app('Profile', icon ="👨🏻‍💼", app=ProfilePage())

app.run()
