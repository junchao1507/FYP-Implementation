# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:44:38 2022

@author: Lenovo
"""

# Importing packages
import pandas as pd
from datetime import datetime
import datetime
import smtplib
import streamlit as st
from hydralit import HydraHeadApp



class ExamDashboardPage(HydraHeadApp):    
    def run(self):
        if 'this_exam' not in st.session_state:
            st.session_state.this_exam = ''
        
        line = '''
        ---
        '''
    
        option_tuple = self.get_exam_data()  
        option = st.sidebar.selectbox("Select an Exam Page", option_tuple)
            
        if option == option_tuple[0]:
            opt = st.selectbox("", ("View Exams", "View Questions"))
            if opt == 'View Exams':
                st.header("View Exams")
                view_exams = st.session_state.exams[["exam_id", "exam_title", "num_of_ques", "duration_minutes", "timestamp_created"]].copy()

                view_exams.rename(columns={'exam_id': 'Exam ID',
                                           'exam_title': 'Exam Title',
                                           'num_of_ques': 'Number of Questions',
                                           'duration_minutes': 'Exam Duration (Minutes)',
                                           'timestamp_created': "Timestamp Created"},
                                  inplace=True, errors='raise')
                style = view_exams.style.hide_index()
                st.write(style.to_html(), unsafe_allow_html=True)
                #st.dataframe(st.session_state.exams)
            else:
                st.header("View Questions")
                self.get_all_questions(st.session_state.current_user['user_id'])
        
        elif any(option in i for i in option_tuple):
            st.session_state.this_exam = st.session_state.exams.loc[(st.session_state.exams['exam_title'] == option) &
                                                   (st.session_state.exams['user_id'] == st.session_state.current_user['user_id'])]
            
            st.title(st.session_state.this_exam.iloc[0]['exam_title'])
            st.header('**Progress**')
            status = self.check_exam_completion()
            st.markdown(line)

            col1, col2 = st.columns(2)
                
            with col1:
                
                if status == 2:
                    st.header('Send Exam to Students')
                    self.send_exam_link(st.session_state.this_exam.iloc[0]['exam_title'], 
                                   st.session_state.this_exam.iloc[0]['exam_id'], 
                                   st.session_state.this_exam.iloc[0]['exam_password'], 
                                   st.session_state.current_user['username'], 
                                   st.session_state.current_user['email'])
                
                with st.form(key='exam_info'):
                    st.header('Exam Information')
                    st.write('**Exam ID:** ', st.session_state.this_exam.iloc[0]['exam_id'])
                    st.write('**Exam Title:** ', st.session_state.this_exam.iloc[0]['exam_title'])
                    st.write('**Date of Exam:** ', st.session_state.this_exam.iloc[0]['date'])
                    st.write('**Start Time:** ', st.session_state.this_exam.iloc[0]['start_time'])
                    st.write('**Duration:** ', str(st.session_state.this_exam.iloc[0]['duration_minutes']), ' minutes')
                    st.write('**Number of Questions:** ', str(st.session_state.this_exam.iloc[0]['num_of_ques']))
                    st.write('**Password:** ', '*' * len(st.session_state.this_exam.iloc[0]['exam_password']))
                    btn_refresh = st.form_submit_button(label='Refresh')
                    
                    if btn_refresh:
                        option_tuple = self.get_exam_data()
                        
                   
                st.write()
                


                st.header('**Update Exam Information**')
                update = st.selectbox('', 
                                    ('Update Exam Title',
                                     'Update Date',
                                     'Update Start Time',
                                     'Update Exam Duration (minutes)',
                                     'Update Number of Questions',
                                     'Update Exam Password'))
                

                self.update_exam_info(update, st.session_state.this_exam, st.session_state.exams)
                

                
            with col2:
                
                num_of_ques = st.session_state.this_exam.iloc[0]['num_of_ques']
                num_of_subq = 0
                ques_list = ['Question ' + str(n + 1) for n in range(num_of_ques)]
                ques_tuple = tuple(ques_list)
                st.header('Exam Questions')
                ques = st.selectbox('', ques_tuple)
                
                # Create questions dataframe
                if 'questions' not in st.session_state:
                    st.session_state.questions = pd.DataFrame(columns=['exam_id', 'num_of_subques', 'question_description', 'question_id', 'question_number', 'sub_question_id', 'topic', 'total_marks'])
                

                if any(ques in i for i in ques_tuple):
                    # Load Question
                    st.session_state.questions = self.get_question_data(st.session_state.this_exam.iloc[0]['exam_id'], st.session_state.questions)
                    
                    # Check if the exam_question exists
                    exist = not(st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])].empty)
                    
                    # If exists, load exam data
                    if exist:
                        question_id = st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])]['question_id'].values.item()
                        question_number = int(ques[-1])
                        question_description = st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])]['question_description'].values.item()
                        topic = st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])]['topic'].values.item()
                        num_of_subques = st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])]['num_of_subques'].values.item()
                        total_marks = st.session_state.questions[st.session_state.questions['question_number'] == int(ques[-1])]['total_marks'].values.item()
                        
                        # Create sub_questions dataframe
                        if 'sub_questions' not in st.session_state:
                            st.session_state.sub_questions = pd.DataFrame(columns = ["e1_answer", "e1_answer_total_marks", "e1_marks", "e2_answer", "e2_answer_total_marks", "e2_marks", "e3_answer", "e3_answer_total_marks", "e3_marks", "e4_answer", "e4_answer_total_marks", "e4_marks", "e5_answer", "e5_answer_total_marks", "e5_marks", "entity1", "entity2", "entity3", "entity4", "entity5", "marks", "question_id", "sub_question_description", "sub_question_id", "sub_question_number"])
                
                    
                        # Load subquestions associated with this question
                        st.session_state.sub_questions = self.get_subquestion_data(question_id, st.session_state.sub_questions)
                        num_of_subq = len(st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id])
                        saq_question_number = []
                        
                        if num_of_subq > 0:
                            saq_question_number = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['sub_question_number'].tolist()
                            saq_question_id = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['sub_question_id'].values
                            saq_question_description = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['sub_question_description'].tolist()
                            saq_e1 = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['entity1'].tolist()
                            saq_e1_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e1_marks'].tolist()
                            saq_e1_answer_total_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e1_answer_total_marks'].tolist()
                            saq_e1_answer = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e1_answer'].tolist()
                            saq_e2 = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['entity2'].tolist()
                            saq_e2_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e2_marks'].tolist()
                            saq_e2_answer_total_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e2_answer_total_marks'].tolist()
                            saq_e2_answer = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e2_answer'].tolist()
                            saq_e3 = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['entity3'].tolist()
                            saq_e3_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e3_marks'].tolist()
                            saq_e3_answer_total_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e3_answer_total_marks'].tolist()
                            saq_e3_answer = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e3_answer'].tolist()
                            saq_e4 = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['entity4'].tolist()
                            saq_e4_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e4_marks'].tolist()
                            saq_e4_answer_total_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e4_answer_total_marks'].tolist()
                            saq_e4_answer = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e4_answer'].tolist()
                            saq_e5 = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['entity5'].tolist()
                            saq_e5_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e5_marks'].tolist()
                            saq_e5_answer_total_marks = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e5_answer_total_marks'].tolist()
                            saq_e5_answer = st.session_state.sub_questions[st.session_state.sub_questions['question_id'] == question_id]['e5_answer'].tolist()
                        

                    # num_of_subq will be at least 1 even if there is no sub questions
                    if num_of_subq == 1 and (len(saq_question_number) == 0 or saq_question_number[0] == 0):
                        #st.write('num_of_subq will be at least 1 even if there is no sub questions')
                        num_of_subq = 0
                    
                            
                    # That question has not been created
                    if not exist:
                        #st.write('That question has not been created')
                        choice = st.radio("How do you want to create this question?", ("Add an existing question", "Constructs a new question"))
                        
                        if choice == "Add an existing question":
                            self.add_existing_question(ques, st.session_state.this_exam.iloc[0]['exam_id'])
                        else:
                            self.create_question(ques, st.session_state.this_exam.iloc[0]['exam_id'])
                        
                    # That question has been created but there's no answer, keywords, and marks allocated.
                    elif total_marks == 0:
                        #st.write("That question has been created but there's no answer, keywords, and marks allocated.")
                        self.display_question_info(question_id, question_number, question_description, topic, num_of_subques, total_marks)
                        self.create_saq(num_of_subq, ques, question_id, num_of_subques)

                        
                        
                    # All subquestions of that question have been created (the question creation is completed)
                    elif num_of_subques == num_of_subq:
                        #st.write("All subquestions of that question have been created (the question creation is completed)")
                        self.display_question_info(question_id, question_number, question_description, topic, num_of_subques, total_marks)
                        
                        # That question has no sub-questions
                        if num_of_subq == 0:
                            #st.write("That question has no sub-questions")
                            if len(saq_question_number) > 0:
                                self.display_saq_q(question_id, saq_question_id, saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
                                                   saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
                                                   saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer)
                                
                        # That question has sub-questions
                        else:
                            #st.write("That question has sub-questions")
                            #for i in range(len(mcq_question_number) + len(saq_question_number)):
                            for i in range(len(saq_question_number)):
                                q_num = i + 1
                    
                    
                                if any(num in str(q_num) for num in str(saq_question_number)):
                                    idx = saq_question_number.index(q_num)
                                    self.display_saq_subq(idx, question_id, saq_question_id, question_number, saq_question_number, saq_question_description, 
                                                          saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
                                                          saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
                                                          saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer)
                        
                    # At least one sub-question have not been created        
                    else:
                        self.display_question_info(question_id, question_number, question_description, topic, num_of_subques, total_marks)
                        
                        for i in range(len(saq_question_number)):
                            q_num = i + 1
                
                
                            if any(num in str(q_num) for num in str(saq_question_number)):
                                idx = saq_question_number.index(q_num)
                                self.display_saq_subq(idx, saq_question_id, question_number, saq_question_number, saq_question_description, 
                                                      saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
                                                      saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
                                                      saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer)

                                
                        self.create_saq(q_num, ques, question_id, num_of_subq)
                
            st.markdown('**________________________________________________________________________________________________**')
            
            
    def get_all_questions(self, user_id):
        # Check if there's exam records in the firebase
        if st.session_state.db.child('exams').shallow().get().val():
            exams_dict = st.session_state.db.child("exams").order_by_child("timestamp_created").order_by_child("user_id").equal_to(user_id).get()
    
        questions = []
        
        # Loop through each exam records and extend the question_ids to the questions list
        for e in exams_dict.each():
            questions.extend(e.val()['questions'])
        
            
        # Remove duplicated values (one question shared by multiple exams)
        questions = list(dict.fromkeys(questions))
        temp_question = pd.DataFrame(columns=['question_id', 'question_description', 'num_of_subques',  'sub_question_id', 'topic', 'total_marks', 'exam_id'])
        
        # Check if there's questions records in the firebase
        if st.session_state.db.child('questions').shallow().get().val():
            # Loop through the question_ids
            for question in questions:
                questions_dict = st.session_state.db.child("questions").order_by_child("question_id").equal_to(question).get()
                
                # For each question, 
                for q in questions_dict.each():
                    # Check if sub_question child exists,
                    if st.session_state.db.child('questions').child(question).child('sub_question_id').shallow().get().val():
                        actual_num_of_subq = len(q.val()['sub_question_id'])
                        assigned_num_of_subq = q.val()['num_of_subques']
                        
                        # Check if the question creation is complete.
                        if actual_num_of_subq > 0 or actual_num_of_subq == assigned_num_of_subq:
                            temp_question = temp_question.append(q.val(), ignore_index = True)
                
        #st.write(temp_question)
        
        view_questions = temp_question[["question_id", "question_description", "topic", "total_marks"]].copy()
        view_questions .rename(columns={'question_id': 'Question ID',
                                        'question_description': 'Question Description',
                                        'topic': 'Topic',
                                        'total_marks': 'Total Marks'},
                               inplace=True, errors='raise')
        
        filter_list = view_questions['Topic'].unique()
        filter_list = filter_list.tolist()
        filter_list.insert(0, 'All')
        filter_tuple = tuple(filter_list)
        filter_topics = st.selectbox("Filter by topic", filter_tuple)
        
        if filter_topics != 'All':
            view_questions = view_questions[(view_questions['Topic'] == filter_topics)] 
            
        style = view_questions.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)
            
            
            
    def send_exam_link(self, exam_title, exam_id, exam_password, instructor_name, instructor_email):
        website_email = 'automated.exam.marking.system@gmail.com'
        email_password = 'isajaoxknpcsvygq'
        exam_link = 'https://share.streamlit.io/junchao1507/fyp-implementation-exam-website/main/Main.py'
        body_message = 'Dear Student,\n\nKindly click on the exam link below and fill up the required details to sit for the examination.\n\nExam Title: '+ exam_title +'\n\nExam Link: '+ exam_link +'\n\nExam Id: '+ exam_id +'\n\nExam Password: '+ exam_password+ "\n\nShould you be facing any difficulties, please do not hesitate to reach out to your teacher " + instructor_name + " via " + instructor_email + ".\n\nAll the best in your examination.\n\nPlease do not reply to this email as it is autogenerated by the system."
        
        with st.form('Send Examination'):
            email_list = st.text_area('Student Email List (separated by a comma):')
            sub = st.text_input('Subject: ', value =  exam_title + ' Link & Password')
            email_body = st.text_area('Email Body:', body_message)
            btn_send = st.form_submit_button('Send Email')
            
            
        if btn_send:
            emails = email_list.split(",")
            emails = [e.replace(' ', '') for e in emails]
            
            sent_from = website_email
            to = emails
            subject = sub
            body = email_body
        
            email_text = 'Subject: {}\n\n{}'.format(subject, body)
            
            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(website_email, email_password)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                st.success("Email sent successfully!")
            except Exception as ex:
                st.error("Something went wrong….",ex)
            
            
    
    def check_exam_completion(self):
        exam_id = st.session_state.this_exam.iloc[0]['exam_id']
        num_of_ques = st.session_state.this_exam.iloc[0]['num_of_ques']
        question = st.session_state.db.child("questions").order_by_child("exam_id").get()
        
        question_id = []
        num_of_subques = []
        # Loading question information
        for q in question.each():
            for eid in q.val()['exam_id']:
                if eid == exam_id:
                    question_id.append(q.val()['question_id'])
                    num_of_subques.append(q.val()['num_of_subques'])
            
        num_of_saq = []
        question_status = []
        total_q_to_be_created = 0

        
        # For each question
        for qid in question_id:
            # If saq exists in the firebase
            if st.session_state.db.child('saq_sub_questions').shallow().get().val():
                # Load all saq linked to the current question
                saq = st.session_state.db.child("saq_sub_questions").order_by_child("sub_question_number").order_by_child("question_id").equal_to(qid).get()
                
                # Count how many saq linked to the current questions (to compare with how many saq should be created for the current question)
                count = 0
                for sq in saq.each():
                    count += 1
                    
                num_of_saq.append(count)
                total_q_to_be_created += count
        

        total_created = []
        total_to_be_created = []
        # Append the total number of questions created to the first index
        total_created.append(len(question_id))
        # Append the total number of questions (supposed to be created) to the first index
        total_to_be_created.append(num_of_ques)
        
        # Status = 0, not all questions completed
        # Status = 1, all questions completed but not all subquestions completed
        # Status = 2, all questions & subquestions completed
        status = 0
        
        # If all questions supposed to be created are created
        if len(question_id) == num_of_ques:
            status = 1
            # Assign the number of saq (created) to the total_created variable
            total_created += num_of_saq
            # Assign the number of subques (supposed to be created) to the total to be created variable
            total_to_be_created += num_of_subques
            # Check if all sub-questions under each question has been created
            for i in range(len(total_to_be_created)):
                # Index 0 stored the question itself
                # Index 1 onwards stored subquestions
                # Even if the question does not have any sub questions
                # There will still be one saq creared and associated with it
                # That's why if that happens, we will assign 0 to total created (originally 1)
                if i > 0 and total_to_be_created[i] == 0:
                    total_created[i] = 0
        
                # Check if all questions (index = 0) and subquestions (index > 0), have been created
                if total_to_be_created[i] == total_created[i]:
                    question_status.append(True)
                else:
                    question_status.append(False)
                    
            # The first index of question_status is for the question itself. Others are subquestions
            if question_status.count(True) == num_of_ques + 1:
                status = 2

                    
        
        completed_percentage = sum(total_created) / sum(total_to_be_created) * 100
        #st.write(str(completed_percentage) + '%')
        st.progress(int(completed_percentage))
        
        if status == 0:
            st.warning(str(num_of_ques - len(question_id)) + ' more question(s) to be created.')
        elif status == 1:
            incomplete = []
            for i, s in enumerate(question_status):
                if s == False:
                    incomplete.append('Question ' + str(i))
                    

            inc_txt = ', '.join(incomplete)
            st.warning('All Questions created but subquestions of these questions are not completed: ' + inc_txt)
        else:
            st.success('Examination Setup is Complete. You can send this exam to your students!')
            
        return status

        
        
                        
    def get_exam_data(self):
        exams_dict = None
        option_list = []
        
        if st.session_state.db.child('exams').shallow().get().val():
            exams_dict = st.session_state.db.child("exams").order_by_child("timestamp_created").order_by_child("user_id").equal_to(st.session_state.current_user['user_id']).get()
        
        
        
        for i, exam in enumerate(exams_dict.each()):
            option_list.append(exam.val()['exam_title'])
            temp_exam = pd.DataFrame(columns = ['exam_id', 'exam_password', 'exam_title', 'num_of_ques', 'questions', 'duration_minutes', 'start_time', 'timestamp_created', 'user_id'])
            unique = None
            
            if st.session_state.exams.empty == True:
                unique = exam.val()
            else:
                temp_exam = temp_exam.append(exam.val(), ignore_index = True)
                unique = temp_exam[~temp_exam["exam_id"].isin(st.session_state.exams["exam_id"])]
                
            if len(unique) > 0:
                st.session_state.exams = st.session_state.exams.append(unique, ignore_index=True)
            
        option_list.insert(0, 'Exam Info')
        option_tuple = tuple(option_list)
    
        return option_tuple
    
    
    
    def get_question_data(self, exam_id, questions):
        questions_dict = None
        if st.session_state.db.child('questions').shallow().get().val():
            questions_dict = st.session_state.db.child("questions").order_by_child("exam_id").get()
            
            # Drop the previous record to avoid duplicated records (two exams can have two questions 1's)
            i = 0
            questions.drop(questions.index[:], inplace=True)
            for question in questions_dict.each():
                for eid in question.val()['exam_id']:
                    if eid == exam_id:
                        i += 1
                        unique = None
                        temp_question = pd.DataFrame(columns=['exam_id', 'num_of_subques', 'question_description', 'question_id', 'question_number', 'sub_question_id', 'topic', 'total_marks'])
                        
                        if questions.empty == True:
                            unique = question.val()
                            unique['question_number'] =  i
                        else:
                            temp_question = temp_question.append(question.val(), ignore_index = True)
                            unique = temp_question[~temp_question["question_id"].isin(questions["question_id"])]
                            unique['question_number'] =  i
                            
                        if len(unique) > 0:
                            questions = questions.append(unique, ignore_index = True)
                    
        return questions



    def get_subquestion_data(self, question_id, sub_questions):
        sub_questions_dict = None
        if st.session_state.db.child('saq_sub_questions').shallow().get().val():
            sub_questions_dict = st.session_state.db.child("saq_sub_questions").order_by_child("question_id").equal_to(question_id).get()
            
            sub_questions.drop(sub_questions.index[:], inplace=True)
            for sub_question in sub_questions_dict.each():
                unique = None
                temp_sub_question = pd.DataFrame(columns = ["e1_answer", "e1_answer_total_marks", "e1_marks", "e2_answer", "e2_answer_total_marks", "e2_marks", "e3_answer", "e3_answer_total_marks", "e3_marks", "e4_answer", "e4_answer_total_marks", "e4_marks", "e5_answer", "e5_answer_total_marks", "e5_marks", "entity1", "entity2", "entity3", "entity4", "entity5", "marks", "question_id", "sub_question_description", "sub_question_id", "sub_question_number"])
                
                if sub_questions.empty == True:
                    unique = sub_question.val()

                else:
                    temp_sub_question = temp_sub_question.append(sub_question.val(), ignore_index = True)
                    unique = temp_sub_question[~temp_sub_question["sub_question_id"].isin(sub_questions["sub_question_id"])]
                    
                if len(unique) > 0:
                    sub_questions = sub_questions.append(unique, ignore_index = True)

        return sub_questions
    
    


    def update_exam_info(self, menu, this_exam, df_exams):
        form_name = menu.lower().replace(" ", "_") + '_form'
        menu_name = menu.replace("Update ", "")
        
        #current_menu = 'Current ' + menu_name + ': '
        new_menu = 'New ' + menu_name + ': '
        
        menu_name_lower = ''
        if menu == 'Update Exam Duration (minutes)':
            menu_name_lower = 'duration_minutes'
            
        elif menu == 'Update Number of Questions':
            menu_name_lower = 'num_of_ques'
            
        else:
            menu_name_lower = menu_name.lower().replace(" ", "_")
            

        if 'new_val' not in st.session_state:
            st.session_state.new_val = ''
        
        with st.form(key=form_name):
            st.markdown("**" + menu + "**")
            
            if menu == 'Update Date':
                if this_exam.iloc[0][menu_name_lower]:
                    v = datetime.datetime.strptime(this_exam.iloc[0][menu_name_lower] , '%Y-%m-%d')
                else:
                    v= None
                st.session_state.new_val = st.date_input(new_menu, value = v).strftime('%Y-%m-%d')
                
            elif menu == 'Update Start Time':
                if this_exam.iloc[0][menu_name_lower]:
                    v = datetime.datetime.strptime(this_exam.iloc[0][menu_name_lower] , '%H:%M:%S')
                else:
                    v= None
                st.session_state.new_val = st.time_input(new_menu, value = v).strftime('%H:%M:%S')
                
            elif menu == 'Update Exam Duration (minutes)' or menu == 'Update Number of Questions':
                st.session_state.new_val = st.number_input(new_menu, min_value=1, value=this_exam.iloc[0][menu_name_lower], step=1) 
                
            elif menu == 'Update Exam Password':
                st.session_state.new_val = st.text_input(new_menu, value = '*' * len(this_exam.iloc[0][menu_name_lower]))
                
            else:
                st.session_state.new_val = st.text_input(new_menu, value=this_exam.iloc[0][menu_name_lower])
                
            btn_submit = st.form_submit_button(label='Submit')
            
        if btn_submit:
            this_exam.at[0, menu_name_lower] = st.session_state.new_val
            this_exam_dict = {menu_name_lower: st.session_state.new_val}
            st.session_state.db.child("exams").child(this_exam.iloc[0]['exam_id']).update(this_exam_dict)
            df_exams.at[df_exams['exam_id'] == this_exam.iloc[0]['exam_id'], menu_name_lower] = st.session_state.new_val
            msg = menu_name +  ' Updated Successfully'
            st.success(msg)
            
            
    
    def add_existing_question(self, ques, exam_id):
        k = 'Re-use Question for ' + ques 
        markdown = '**' + k + '**'
        st.write('')
        st.markdown(markdown)
            
        with st.form(key = k):
            question_id = st.text_input('Question ID:')
            btn_add_ques = st.form_submit_button(label='Add Question')
            
            if btn_add_ques:
                if st.session_state.db.child("questions").child(question_id).shallow().get().val():
                    exam = st.session_state.db.child("exams").order_by_child("exam_id").equal_to(exam_id).get()
                    qid_list = []
    
                    for e in exam.each():
                        if st.session_state.db.child('exams').child(exam_id).child('questions').shallow().get().val():
                            qid_list = e.val()['questions']
                        
                    qid_list.extend([question_id])
                    q_dict = {'questions' : qid_list}
                    st.session_state.db.child("exams").child(exam_id).update(q_dict)
                    
                    question = st.session_state.db.child("questions").order_by_child("question_id").equal_to(question_id).get()
                    eid_list = []
                    
                    for q in question.each():
                        if st.session_state.db.child('questions').child(question_id).child('exam_id').shallow().get().val():
                            eid_list = q.val()['exam_id']
                            
                    eid_list.extend([exam_id])
                    e_dict = {'exam_id' : eid_list}
                    st.session_state.db.child("questions").child(question_id).update(e_dict)
                    st.success('Question Added!')
                    
                    
                else:
                    st.error('This question does not exist!')
        btn_refresh = st.button("Refresh")
            
            
    def create_question(self, ques, exam_id):
        k = 'Construct ' + ques 
        markdown = '**' + k + '**'
        st.write('')
        st.markdown(markdown)
        num_of_subques = 0
        subques = [None] * num_of_subques

        # Form to create questions
        with st.form(key= k):
            question_description = st.text_input('Question Description: ')
            topic = st.text_input('Topic: ')
            chk_submit_ques = st.checkbox('Confirm Submission', value=False)
            btn_submit_ques = st.form_submit_button(label='Proceed')
        
        # Submit question into firebase
        if chk_submit_ques:
            if btn_submit_ques:
                if not question_description:
                    st.error("Please enter a question description.")
                elif not topic:
                    st.error("Please enter a topic.")
                else:
                    q = {
                        'question_description': question_description,
                        'topic': topic,
                        'num_of_subques' : num_of_subques,
                        'sub_question_id' : "",
                        'total_marks': 0,
                        'exam_id': [exam_id]
                        }
                    
                    if 'q_id' not in st.session_state:
                        st.session_state.q_id = ''
                    
                    qu = st.session_state.db.child('questions').push(q)
                    # Set question id 
                    st.session_state.db.child("questions").child(qu['name']).update({"question_id": qu['name']})
                    
                    # Set Get exam_id and append this question to the questionid list
                    exam = st.session_state.db.child("exams").order_by_child("exam_id").equal_to(exam_id).get()
                    qid_list = []
                    for e in exam.each():
                        if st.session_state.db.child('exams').child(exam_id).child('questions').shallow().get().val():
                            qid_list = e.val()['questions']
                        
                    qid_list.extend([qu['name']])
                    q_dict = {'questions' : qid_list}
                    st.session_state.db.child("exams").child(exam_id).update(q_dict)
                    st.session_state.q_id = st.session_state.db.child("questions").child(qu['name']).get().key()
                    st.success('Question Created!')
                    # Function to set answers and marks for the question
                    self.create_saq(0, ques, st.session_state.q_id, num_of_subques)
                
# =============================================================================
#                 # If the question has no subquestions
#                 if num_of_subques == 0:
#                     self.create_saq(0, ques, st.session_state.q_id, num_of_subques)
#                 else:
#                     for i in range(num_of_subques):
#                         self.create_saq(i, ques, st.session_state.q_id, num_of_subques)
# =============================================================================
                        
                        

    
    def create_saq(self, subq_idx, ques, q_id, num_of_subq):
        if num_of_subq > 0:
            markdown = '**' + ques + '(' + chr(97 + subq_idx) + ')**'
            q_desc_markdown =  ques + '(' + chr(97 + subq_idx) + ') Description'
        else: 
            markdown = '**' + ques + '**'
        
        with st.form(key= markdown):
            st.markdown(markdown)
            if num_of_subq > 0:
                st.text_input(q_desc_markdown, key = 'saq_desc')
            st.info('If you have compare and contrust questions, or advantages vs disadvantages questions, please put the answers under different entities. Otherwise, just fill in entity1 will do.')
            st.write()
            st.text_input('Entity 1: ', key='entity1')
            st.number_input('Entity 1 Marks: ', min_value=1, value=1, step=1, key='e1_marks')
            st.text_area('Entity 1 Answer: ', key='e1_saq_answer')
            st.number_input('Entity 1 Answer Total Marks: ', min_value=1, value=1, step=1, key='e1_answer_total_marks')
            st.write()
            st.text_input('Entity 2: ', key='entity2', placeholder="This field is not compulsory")
            st.number_input('Entity 2 Marks: ', min_value=0, value=0, step=1, key='e2_marks')
            st.text_area('Entity 2 Answer: ', key='e2_saq_answer', placeholder="This field is not compulsory")
            st.number_input('Entity 2 Answer Total Marks: ', min_value=1, value=1, step=1, key='e2_answer_total_marks')
            st.write()
            st.text_input('Entity 3: ', key='entity3', placeholder="This field is not compulsory")
            st.number_input('Entity 3 Marks: ', min_value=0, value=0, step=1, key='e3_marks')
            st.text_area('Entity 3 Answer: ', key='e3_saq_answer', placeholder="This field is not compulsory")
            st.number_input('Entity 3 Answer Total Marks: ', min_value=1, value=1, step=1, key='e3_answer_total_marks')
            st.write()
            st.text_input('Entity 4: ', key='entity4', placeholder="This field is not compulsory")
            st.number_input('Entity 4 Marks: ', min_value=0, value=0, step=1, key='e4_marks')
            st.text_area('Entity 4 Answer: ', key='e4_saq_answer', placeholder="This field is not compulsory")
            st.number_input('Entity 4 Answer Total Marks: ', min_value=1, value=1, step=1, key='e4_answer_total_marks')
            st.write()
            st.text_input('Entity 5: ', key='entity5', placeholder="This field is not compulsory")
            st.number_input('Entity 5 Marks: ', min_value=0, value=0, step=1, key='e5_marks')
            st.text_area('Entity 5 Answer: ', key='e5_saq_answer', placeholder="This field is not compulsory")
            st.number_input('Entity 5 Answer Total Marks: ', min_value=1, value=1, step=1, key='e5_answer_total_marks')
            
            btn_submit_saq = st.form_submit_button(label='Submit', on_click=self.submit_saq, args = (num_of_subq, subq_idx, q_id))
            


    def submit_saq(self, num_of_subq, subq_idx, q_id):
        if not st.session_state.entity1:
            st.error("Please enter a label for Entity 1")
        elif not st.session_state.e1_saq_answer:
            st.error("Please enter a value for Entity 1 Answer")
        else:
            if num_of_subq > 0:
                qnum = subq_idx + 1
                qdesc = st.session_state.saq_desc
            else:
                qnum = 0
                qdesc = ''
            # Sub question dictionary (the answers)
            sq = {
                'sub_question_number' : qnum,
                'sub_question_description': qdesc,
                'marks': st.session_state.e1_marks + st.session_state.e2_marks + st.session_state.e3_marks + st.session_state.e4_marks + st.session_state.e5_marks,
                
                'entity1' : st.session_state.entity1,
                'e1_marks': st.session_state.e1_marks,
                'e1_answer' : st.session_state.e1_saq_answer,
                'e1_answer_total_marks' : st.session_state.e1_answer_total_marks,
                
                'entity2' : st.session_state.entity2,
                'e2_marks': st.session_state.e2_marks,
                'e2_answer' : st.session_state.e2_saq_answer,
                'e2_answer_total_marks' : st.session_state.e2_answer_total_marks,
                
                'entity3' : st.session_state.entity3,
                'e3_marks': st.session_state.e3_marks,
                'e3_answer' : st.session_state.e3_saq_answer,
                'e3_answer_total_marks' : st.session_state.e3_answer_total_marks,
                
                'entity4' : st.session_state.entity4,
                'e4_marks': st.session_state.e4_marks,
                'e4_answer' : st.session_state.e4_saq_answer,
                'e4_answer_total_marks' : st.session_state.e4_answer_total_marks,
                
                'entity5' : st.session_state.entity5,
                'e5_marks': st.session_state.e5_marks,
                'e5_answer' : st.session_state.e5_saq_answer,
                'e5_answer_total_marks' : st.session_state.e5_answer_total_marks,
                
                'question_id': q_id
                }
            
            # Save the subquestion dictionary into firebase real-time database
            qu = st.session_state.db.child('saq_sub_questions').push(sq)
            st.session_state.db.child("saq_sub_questions").child(qu['name']).update({"sub_question_id": qu['name']})
            sq_dict = {'sub_question_id' : qu['name']}
            st.session_state.db.child("questions").child(q_id).update(sq_dict)
    
            # Update the question's total marks on firebase real-time database
            marks = 0
            ques = st.session_state.db.child("questions").order_by_child("question_id").equal_to(q_id).get()
            for i, q in enumerate(ques.each()):
                marks = q.val()['total_marks']
                
            st.session_state.db.child("questions").child(q_id).update({"total_marks": marks + 
                                                                       st.session_state.e1_marks +
                                                                       st.session_state.e2_marks +
                                                                       st.session_state.e3_marks +
                                                                       st.session_state.e4_marks +
                                                                       st.session_state.e5_marks})
            
            st.success('Sub-Question Created!')
        

    def display_question_info(self, question_id, question_number, question_description, topic, num_of_subques, total_marks):
        with st.form('display_question'):
            st.write('**Question ID:** ' + question_id)
            st.write('**Description:** ' + question_description)
            st.write('**Topic:** ' + topic)
            #st.write('**Number of Sub-Questions:** ' + str(num_of_subques))
            st.write('**Total Marks:** ' + str(total_marks))
            chk_edit = st.checkbox('Edit Question', key='chk_edit')
            btn_edit = st.form_submit_button(label = 'Edit Question')
            
        if chk_edit:
            self.edit_question_info(question_id, question_number, question_description, topic, num_of_subques, total_marks)
                


    def edit_question_info(self, question_id, question_number, question_description, topic, num_of_subques, total_marks):
        with st.form('update_question'):
            info = '**Edit Question ' + str(question_number) + '**'
            st.write(info)
            question_description = st.text_input('Question Description: ', value = question_description)
            topic = st.text_input('Topic: ', value = topic)
            #num_of_subques = st.number_input('Number of Sub-questions: ', min_value=0, value = num_of_subques, step=1)
            #total_marks = st.number_input('Total Marks: ', min_value=0, value=total_marks, step=1)
    
            chk_update_q = st.checkbox('Confirm Submission', key='chk_update_q')
            btn_submit_q = st.form_submit_button('Ok')
        
        
        if chk_update_q:
            self.update_question_(question_id, question_description, topic, num_of_subques, total_marks)
            
            
            
    def update_question_(self, question_id, question_description, topic, num_of_subques, total_marks):
        q = {
            'question_description': question_description,
            'topic' : topic
            }

        st.session_state.db.child("questions").child(question_id).update(q)
        st.success('Update Successfully.')
        btn_done = st.button('Refresh Page', on_click = self.reset_chk_edit)
        
    
        
    def reset_chk_edit(self):
        st.session_state.chk_edit = False
    
    
    def display_saq_q(self, question_id, saq_question_id, saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
                       saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
                       saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer):
        with st.form('display_saq_q'):
            st.write('**Entity 1:** ', saq_e1[0])
            st.write('**Entity 1 Answer:** ', saq_e1_answer[0])
            st.write('**Entity 1 Answer Total Marks:** ', str(saq_e1_answer_total_marks[0]))
            st.write('**Entity 1 Max Marks:** ', str(saq_e1_marks[0]))
            st.write('')
            
            if saq_e2[0]:
                st.write('**Entity 2:** ', saq_e2[0])
                st.write('**Entity 2 Answer:** ', saq_e2_answer[0])
                st.write('**Entity 2 Answer Total Marks:** ', str(saq_e2_answer_total_marks[0]))
                st.write('**Entity 2 Marks:** ', str(saq_e2_marks[0]))
                st.write('')
            
            if saq_e3[0]:
                st.write('**Entity 3:** ', saq_e3[0])
                st.write('**Entity 3 Answer:** ', saq_e3_answer[0])
                st.write('**Entity 3 Answer Total Marks:** ', str(saq_e3_answer_total_marks[0]))
                st.write('**Entity 3 Marks:** ', str(saq_e3_marks[0]))
                st.write('')
            
            if saq_e4[0]:
                st.write('**Entity 4:** ', saq_e4[0])
                st.write('**Entity 4 Answer:** ', saq_e4_answer[0])
                st.write('**Entity 4 Answer Total Marks:** ', str(saq_e4_answer_total_marks[0]))
                st.write('**Entity 4 Marks:** ', str(saq_e4_marks[0]))
                st.write('')
            
            if saq_e5[0]:
                st.write('**Entity 5:** ', saq_e5[0])
                st.write('**Entity 5 Answer:** ', saq_e5_answer[0])
                st.write('**Entity 5 Answer Total Marks:** ', str(saq_e5_answer_total_marks[0]))
                st.write('**Entity 5 Marks:** ', str(saq_e5_marks[0]))
                st.write('')

            chk_edit_saq_q = st.checkbox('Edit Answer')
            btn_edit_saq_q = st.form_submit_button(label = 'Edit Answer')
            
        if chk_edit_saq_q:
            self.edit_saq(question_id, saq_question_id[0], '', saq_e1[0], saq_e1_marks[0], saq_e1_answer_total_marks[0], saq_e1_answer[0], 
            saq_e2[0], saq_e2_marks[0], saq_e2_answer_total_marks[0], saq_e2_answer[0], saq_e3[0], saq_e3_marks[0], saq_e3_answer_total_marks[0], saq_e3_answer[0], 
            saq_e4[0], saq_e4_marks[0], saq_e4_answer_total_marks[0], saq_e4_answer[0], saq_e5[0], saq_e5_marks[0], saq_e5_answer_total_marks[0], saq_e5_answer[0])

        
    
    
    def display_saq_subq(self, idx, question_id, saq_question_number, question_number, saq_question_id, saq_question_description,
                         saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
                       saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
                       saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer):
        k = 'display_saq_subq' + str(idx)

        with st.form(k):
            st.write('**Entity 1:** ', saq_e1[idx])
            st.write('**Entity 1 Answer:** ', saq_e1_answer[idx])
            st.write('**Entity 1 Answer Total Marks:** ', str(saq_e1_answer_total_marks[idx]))
            st.write('**Entity 1 Max Marks:** ', str(saq_e1_marks[idx]))
            st.write('')
            
            if saq_e2[idx]:
                st.write('**Entity 2:** ', saq_e2[idx])
                st.write('**Entity 2 Answer:** ', saq_e2_answer[idx])
                st.write('**Entity 2 Answer Total Marks:** ', str(saq_e2_answer_total_marks[idx]))
                st.write('**Entity 2 Marks:** ', str(saq_e2_marks[idx]))
                st.write('')
            
            if saq_e3[idx]:
                st.write('**Entity 3:** ', saq_e3[idx])
                st.write('**Entity 3 Answer:** ', saq_e3_answer[idx])
                st.write('**Entity 3 Answer Total Marks:** ', str(saq_e3_answer_total_marks[idx]))
                st.write('**Entity 3 Marks:** ', str(saq_e3_marks[idx]))
                st.write('')
            
            if saq_e4[idx]:
                st.write('**Entity 4:** ', saq_e4[idx])
                st.write('**Entity 4 Answer:** ', saq_e4_answer[idx])
                st.write('**Entity 4 Answer Total Marks:** ', str(saq_e4_answer_total_marks[idx]))
                st.write('**Entity 4 Marks:** ', str(saq_e4_marks[idx]))
                st.write('')
            
            if saq_e5[idx]:
                st.write('**Entity 5:** ', saq_e5[idx])
                st.write('**Entity 5 Answer:** ', saq_e5_answer[idx])
                st.write('**Entity 5 Answer Total Marks:** ', str(saq_e5_answer_total_marks[idx]))
                st.write('**Entity 5 Marks:** ', str(saq_e5_marks[idx]))
                st.write('')

            display = 'Edit ' + str(question_number) + '(' + chr(97 + idx) + ')'
            chk_edit_saq_subq = st.checkbox(label = display, key='chk_edit_saq_subq')
            btn_edit_saq_subq = st.form_submit_button(label = display + ')')
            
            
        if chk_edit_saq_subq:
            self.edit_saq(question_id, saq_question_id[idx], saq_question_description[idx], saq_e1[idx], saq_e1_marks[idx], saq_e1_answer_total_marks[idx], saq_e1_answer[idx], 
            saq_e2[idx], saq_e2_marks[idx], saq_e2_answer_total_marks[idx], saq_e2_answer[idx], saq_e3[idx], saq_e3_marks[idx], saq_e3_answer_total_marks[idx], saq_e3_answer[idx], 
            saq_e4[idx], saq_e4_marks[idx], saq_e4_answer_total_marks[idx], saq_e4_answer[idx], saq_e5[idx], saq_e5_marks[idx], saq_e5_answer_total_marks[idx], saq_e5_answer[idx])
                
        
    
    def edit_saq(self, question_id, saq_question_id, ques_desc, saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
    saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
    saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer):
        
        with st.form('update_saq'):
# =============================================================================
#             if not ques_desc:
#                 ques_desc = st.text_input('Question Description: ', key = 'update_ques_desc', value = ques_desc)
# =============================================================================
            
            st.info('If you have compare and contrust questions, or advantages vs disadvantages questions, please put the answers under different entities. Otherwise, just fill in entity1 will do.')
            saq_e1 = st.text_input('Entity 1: ', value = saq_e1, key = 'saq_e1')
            #saq_e1_keywords = st.text_input('Entity 1 Keywords: ', value = saq_e1_keywords, key='saq_e1_keywords')
            saq_e1_answer = st.text_input('Entity Answer: ', value = saq_e1_answer, key='saq_e1_answer')
            saq_e1_marks = st.number_input('Entity 1 Marks: ', min_value=1, value=saq_e1_marks, step=1, key='saq_e1_marks')
            saq_e1_answer_total_marks = st.number_input('Entity 1 Answer Total Marks: ', min_value=1, value=saq_e1_answer_total_marks, step=1, key='saq_e1_answer_total_marks')
            st.write('')
            
            saq_e2 = st.text_input('Entity 2: ', value = saq_e2, key = 'saq_e2')
            #saq_e2_keywords = st.text_input('Entity 2 Keywords: ', value = saq_e2_keywords, key='saq_e2_keywords')
            saq_e2_answer = st.text_input('Entity Answer: ', value = saq_e2_answer, key='saq_e2_answer')
            saq_e2_marks = st.number_input('Entity 2 Marks: ', min_value=0, value=saq_e2_marks, step=1, key='saq_e2_marks')
            saq_e2_answer_total_marks = st.number_input('Entity 2 Answer Total Marks: ', min_value=0, value=saq_e2_answer_total_marks, step=1, key='saq_e2_answer_total_marks')
            st.write('')

            saq_e3 = st.text_input('Entity 3: ', value = saq_e3, key = 'saq_e3')
            #saq_e3_keywords = st.text_input('Entity 3 Keywords: ', value = saq_e3_keywords, key='saq_e3_keywords')
            saq_e3_answer = st.text_input('Entity Answer: ', value = saq_e3_answer, key='saq_e3_answer')
            saq_e3_marks = st.number_input('Entity 3 Marks: ', min_value=0, value=saq_e3_marks, step=1, key='saq_e3_marks')
            saq_e3_answer_total_marks = st.number_input('Entity 3 Answer Total Marks: ', min_value=0, value=saq_e3_answer_total_marks, step=1, key='saq_e3_answer_total_marks')
            st.write('')
            
            saq_e4 = st.text_input('Entity 4: ', value = saq_e4, key = 'saq_e4')
            #saq_e4_keywords = st.text_input('Entity 4 Keywords: ', value = saq_e4_keywords, key='saq_e4_keywords')
            saq_e4_answer = st.text_input('Entity Answer: ', value = saq_e4_answer, key='saq_e4_answer')
            saq_e4_marks = st.number_input('Entity 4 Marks: ', min_value=0, value=saq_e4_marks, step=1, key='saq_e4_marks')
            saq_e4_answer_total_marks = st.number_input('Entity 4 Answer Total Marks: ', min_value=0, value=saq_e4_answer_total_marks, step=1, key='saq_e4_answer_total_marks')
            st.write('')
            
            saq_e5 = st.text_input('Entity 5: ', value = saq_e5, key = 'saq_e5')
            #saq_e5_keywords = st.text_input('Entity 5 Keywords: ', value = saq_e5_keywords, key='saq_e5_keywords')
            saq_e5_answer = st.text_input('Entity Answer: ', value = saq_e5_answer, key='saq_e5_answer')
            saq_e5_marks = st.number_input('Entity 5 Marks: ', min_value=0, value=saq_e5_marks, step=1, key='saq_e5_marks')
            saq_e5_answer_total_marks = st.number_input('Entity 5 Answer Total Marks: ', min_value=0, value=1, step=saq_e5_answer_total_marks, key='saq_e5_answer_total_marks')
            st.write('')
        
            #chk_update_saq = st.checkbox('Confirm Submission', key='chk_update_saq')
            btn_submit_saq = st.form_submit_button('Ok')
            
        if btn_submit_saq:
            self.update_saq_(question_id, saq_question_id, ques_desc, saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
            saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
            saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer)
                
    
    def update_saq_(self, question_id, saq_question_id, ques_desc, saq_e1, saq_e1_marks, saq_e1_answer_total_marks, saq_e1_answer, saq_e2, saq_e2_marks, saq_e2_answer_total_marks, saq_e2_answer, 
    saq_e3, saq_e3_marks, saq_e3_answer_total_marks, saq_e3_answer, saq_e4, saq_e4_marks,saq_e4_answer_total_marks, saq_e4_answer,
    saq_e5, saq_e5_marks, saq_e5_answer_total_marks, saq_e5_answer):
        
        
        saq={
            'sub_question_description': ques_desc,
            'marks': saq_e1_marks + saq_e2_marks + saq_e3_marks + saq_e4_marks + saq_e5_marks,
            
            'entity1' : saq_e1,
            'e1_marks': saq_e1_marks,
            'e1_answer' : saq_e1_answer,
            'e1_answer_total_marks' : saq_e1_answer_total_marks,
            
            'entity2' : saq_e2,
            'e2_marks': saq_e2_marks,
            'e2_answer' : saq_e2_answer,
            'e2_answer_total_marks' : saq_e2_answer_total_marks,
            
            'entity3' : saq_e3,
            'e3_marks': saq_e3_marks,
            'e3_answer' : saq_e3_answer,
            'e3_answer_total_marks' : saq_e3_answer_total_marks,
            
            'entity4' : saq_e4,
            'e4_marks': saq_e4_marks,
            'e4_answer' : saq_e4_answer,
            'e4_answer_total_marks' : saq_e4_answer_total_marks,
            
            'entity5' : saq_e5,
            'e5_marks': saq_e5_marks,
            'e5_answer' : saq_e5_answer,
            'e5_answer_total_marks' : saq_e5_answer_total_marks
            }
        
        q = {
            'total_marks' : saq_e1_marks + saq_e2_marks + saq_e3_marks + saq_e4_marks + saq_e5_marks
        }
        
        st.session_state.db.child("sub_question_id").child(saq_question_id).update(saq)
        st.session_state.db.child("questions").child(question_id).update(q)
        st.success('Updated Successfully.')
        btn_done = st.button('Refresh Page', on_click = self.reset_chk_edit_saq_subq)
        
    def reset_chk_edit_saq_subq(self):
        st.session_state.chk_edit_saq_subq = False