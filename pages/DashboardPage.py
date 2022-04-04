# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:27:46 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp
from PIL import Image


import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import smtplib


class DashboardPage(HydraHeadApp): 
    def run(self):
        
        # Save variables into session state
        if 'view_this_exam' not in st.session_state:
            st.session_state.view_this_exam = ''
            
        if 'df_questions' not in st.session_state:
            st.session_state.df_question = None
            
        if 'question' not in st.session_state:
            st.session_state.question = None
            
        if 'student_id' not in st.session_state:
            st.session_state.student_id = None
            
        if 'df_answers' not in st.session_state:
            st.session_state.df_answers = None
            
        if 'df_results' not in st.session_state:
            st.session_state.df_results = None
            
        if 'df_this_question' not in st.session_state:
            st.session_state.df_this_question = None
            
        if 'sub_question_id' not in st.session_state:
            st.session_state.sub_question_id = ''
            
            
        
        grade_list = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]
        passling_grade_list = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
        gradedict = {grade: i for i, grade in enumerate('A+ A A- B+ B B- C+ C D F'.split())}
        gp_list = [4.33, 4.00, 3.67, 3.33, 3.00, 2.67, 2.33, 2.00, 1.00, 0.00]
        cut_off_list = [85, 80, 75, 70, 65, 60, 55, 50, 40, 0]
        status_list = ["PASS", "FAIL"]
            

        line = '''
        ---
        '''

        
        
        # Set option tuple (all exams loaded)
        option_tuple = self.get_exam_data()  
        option = st.sidebar.selectbox("Select an Exam", option_tuple)
        
        
        
        # Dashboard page
        if option == option_tuple[0]:
            st.markdown("<h1 style='text-align: center; line-height: 120px;'>Exam Analytics Dashboard Page</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; line-height: 120px;'>Select an Exam Title on the sidebar</h3>", unsafe_allow_html=True)
            image = "https://raw.githubusercontent.com/junchao1507/FYP-Implementation/main/images/ComputerGrading4.jpg"
            st.image(image, caption='', width=1450)
        
        elif any(option in i for i in option_tuple):
            st.session_state.view_this_exam = st.session_state.exams.loc[(st.session_state.exams['exam_title'] == option) &
                                                   (st.session_state.exams['user_id'] == st.session_state.current_user['user_id'])]
            

            
            # Get exam questions and students answers for this exam
            st.session_state.df_questions, st.session_state.df_answers = self.get_questions_and_answers(st.session_state.current_user['user_id'], st.session_state.view_this_exam.iloc[0]['exam_id'])


            if (not st.session_state.df_answers.empty) and (len(st.session_state.df_answers) == len(st.session_state.df_answers.loc[st.session_state.df_answers['verified'] == 1])):
                st.session_state.df_results, exam_full_marks = self.get_students_results(st.session_state.df_answers, grade_list, gp_list)
                number_of_candidates, pass_rate, average_marks, average_gp = self.display_exam_stats(st.session_state.df_results)

                # Set student tuple
                studentid_list = st.session_state.df_answers['student_id'].unique()
                studid_tuple = tuple(studentid_list)
                st.session_state.student_id = st.sidebar.selectbox("Select a Student Id", (studid_tuple))
    
    
                # Set the question tuple (load all exam questions)
                ques_tuple = [ "Question " + str(i + 1) for i in range(len(st.session_state.df_questions))]
                st.session_state.question = st.sidebar.selectbox("Select Exam Question", (ques_tuple))
                st.session_state.df_this_question = st.session_state.df_answers[st.session_state.df_answers['sub_question_id'] == st.session_state.df_questions.iloc[int(st.session_state.question[-1]) - 1]['sub_question_id']]
                st.session_state.df_this_question = st.session_state.df_this_question.reset_index(drop=True)
                raw_mean_marks = float(format(st.session_state.df_this_question['score'].mean(), ".2f"))
                full_marks = st.session_state.df_this_question.iloc[0]['total_marks']
            
                # Dashboard Layout
                title_markdown = "<h1 style='text-align: center; line-height: 120px;'>" + st.session_state.view_this_exam.iloc[0]['exam_title'] + " Dashboard</h1>"
                st.markdown(line)
                st.markdown(title_markdown, unsafe_allow_html=True)
                
                
                
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        fig0 = go.Figure()
                        fig0.add_trace(go.Indicator(
                            mode = "number",
                            number = {'font': {'size': 65}},
                            value = len(st.session_state.df_this_question),
                            title = {"text": "<b>Number of Candidates<b>"},
                            ))
                        
                        fig0.update_layout(height=120)
                        
                        st.plotly_chart(fig0, use_container_width=True)
                        
                    with col2:
                        fig1 = go.Figure()
                        fig1.add_trace(go.Indicator(
                            mode = "number",
                            number = {'suffix': "%", 'font': {'size': 65}},
                            value = pass_rate,
                            title = {"text": "<b>Passing Rate<b>"},
                            ))
                        
                        fig1.update_layout(height=120)
    
                        st.plotly_chart(fig1, use_container_width=True)
                            
                    with col3:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Indicator(
                            mode = "number",
                            number = {'suffix': "%", 'font': {'size': 65}},
                            value = average_marks,
                            title = {"text": "<b>Average Marks (%)<b>"},
                            ))
                        
                        fig2.update_layout(height=120)
                        
                        st.plotly_chart(fig2, use_container_width=True)
                        
                    with col4:
                        fig3 = go.Figure()
                        fig3.add_trace(go.Indicator(
                            mode = "number",
                            number = {'font': {'size': 65}},
                            value = average_gp,
                            title = {"text": "<b>Average Grade Point<b>"},
                            ))
                        
                        fig3.update_layout(height=120)
                        
                        st.plotly_chart(fig3, use_container_width=True)
        
        
                with st.container():
                    col5, col6 = st.columns(2)
                    with col5:
                        self.display_grade_distribution(st.session_state.df_results, gp_list, grade_list, status_list)
                        
                        
                    with col6:
                        self.display_question_performance("Performance by Question (%)", st.session_state.df_answers)
                
                
                with st.container():
                    blk, col7, blk, col8 = st.columns([0.5, 4, 0.5, 5])
                    
                    with col7:
                        title_markdown = '<div style="text-align:center;"><span style="font-weight:bold; line-height: 50px;">Students Scores</span></div>'
                        st.markdown(title_markdown, unsafe_allow_html=True)
                        st.dataframe(st.session_state.df_results.style.format(subset=['score', 'grade_point'], formatter="{:.2f}"), width=5000)
                        csv = self.convert_df(st.session_state.df_results)
                        st.download_button(
                            label = 'Download as CSV', 
                            data = csv, 
                            file_name= st.session_state.view_this_exam.iloc[0]['exam_title'] + '.csv',
                            mime = 'text/csv')
                        
                        
                    with col8:
                        df_temp_stud = st.session_state.df_answers[st.session_state.df_answers['student_id'] == st.session_state.student_id]
                        df_temp_stud = df_temp_stud.set_index('sub_question_id')
                        df_temp_stud = df_temp_stud.reindex(index=st.session_state.df_questions['sub_question_id'])
                        df_temp_stud = df_temp_stud.reset_index()
                        
                        attr = ["e1_answer", "e1_answer_total_marks", "e1_marks", "e2_answer", "e2_answer_total_marks", "e2_marks", "e3_answer", "e3_answer_total_marks", "e3_marks", "e4_answer", "e4_answer_total_marks", "e4_marks", "e5_answer", "e5_answer_total_marks", "e5_marks", "entity1", "entity2", "entity3", "entity4", "entity5", "marks", "question_id", "sub_question_description", "sub_question_id", "sub_question_number"]
                        
                        for a in attr:
                            df_temp_stud[a] = np.where(df_temp_stud['sub_question_id'] == st.session_state.df_questions['sub_question_id'], st.session_state.df_questions[a], "")

                        title = st.session_state.student_id + " Performance by Question (%)"
                        self.display_students_question_performance(title, df_temp_stud)
                
                
                with st.container():
                    title = st.session_state.question + " Analytics"
                    title_markdown = "<h2 style='text-align: center; line-height: 120px;'>" + title + "</h2>"
                    st.markdown(title_markdown, unsafe_allow_html=True)
    
    
                
                with st.container():
                    
                    col9, col10 = st.columns([1.5,2.5])
                    
                    with col9:
                        st.write("\n")
                        q_pass_rate = self.get_question_passing_rate(st.session_state.df_answers, st.session_state.df_this_question.iloc[0]['sub_question_id'])
                        
                        fig4 = go.Figure()
    
                        fig4.add_trace(go.Indicator(
                            mode = "number",
                            number = {'suffix': "%", 'font': {'size': 65}},
                            value = q_pass_rate * 100,
                            title = {"text": "<b>Passing Rate (%)<b>"},
                            ))
                        
                        fig4.update_layout(
                            height=120,  # Added parameter
                        )
                        
                        st.plotly_chart(fig4, use_container_width=True)
                        
                        
                        self.display_average_mark_speedometer(st.session_state.question + " Average Score", raw_mean_marks, full_marks)
                        
                    with col10:
                        self.display_marks_distribution(" Marks Distribution", st.session_state.df_this_question)
                        
                        
                with st.container():
                    self.send_feedback_email(studentid_list, st.session_state.df_questions, st.session_state.df_answers, st.session_state.df_results)
                        
            else:
                st.warning("Exam Marking has not finished or Exam has not been held.")
                    
                    
                
                
                    
    def convert_df(self, df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
                
                
                
            
    def get_exam_data(self):
        exams_dict = None
        option_list = []
        
        if st.session_state.db.child('exams').shallow().get().val():
            exams_dict = st.session_state.db.child("exams").order_by_child("timestamp_created").order_by_child("user_id").equal_to(st.session_state.current_user['user_id']).get()
        
        
        
        for i, exam in enumerate(exams_dict.each()):
            option_list.append(exam.val()['exam_title'])
            temp_exam = pd.DataFrame(columns = ['exam_id', 'exam_password', 'exam_title', 'num_of_ques', 'total_marks', 'questions', 'duration_minutes', 'start_time', 'timestamp_created', 'user_id'])
            unique = None
            
            if st.session_state.exams.empty == True:
                unique = exam.val()
            else:
                temp_exam = temp_exam.append(exam.val(), ignore_index = True)
                unique = temp_exam[~temp_exam["exam_id"].isin(st.session_state.exams["exam_id"])]
                
            if len(unique) > 0:
                st.session_state.exams = st.session_state.exams.append(unique, ignore_index=True)
            
        option_list.insert(0, 'Select an Exam')
        option_tuple = tuple(option_list)
    
        return option_tuple
    
    
    
    def get_questions_and_answers(self, user_id, exam_id):
        # Check if there's exam records in the firebase
        if st.session_state.db.child('exams').shallow().get().val():
            exams_info = st.session_state.db.child("exams").order_by_child("exam_id").equal_to(exam_id).get()
    
            question_id_list = []
            
            for e in exams_info.each():
                exam_id = e.val()['exam_id']
                question_id_list.extend(e.val()['questions'])
                
            subquestion_id_list = []
            topics_list = []
            total_marks_list = []
            question_list = []
            for question_id in question_id_list:
                question_info = st.session_state.db.child("questions").order_by_child("question_id").equal_to(question_id).get()
                
                for q in question_info.each():
                    subquestion_id_list.extend(q.val()['sub_question_id'])
                    topics_list.append(q.val()['topic'])
                    total_marks_list.append(q.val()['total_marks'])
                    question_list.append(q.val())
                    
            df_questions = pd.DataFrame(question_list, columns=['question_id', 'question_description', 'num_of_subques',  'sub_question_id', 'topic', 'total_marks', 'exam_id'])
                    
            data = []
            for i, row in df_questions.iterrows():
                subquestions = st.session_state.db.child("saq_sub_questions").child(row["sub_question_id"]).get()
                
                d = []
                for sq in subquestions.each():
                    d.append(sq.val())
                data.append(d)
                
            df_questions[["e1_answer", "e1_answer_total_marks", "e1_marks", "e2_answer", "e2_answer_total_marks", "e2_marks", "e3_answer", "e3_answer_total_marks", "e3_marks", "e4_answer", "e4_answer_total_marks", "e4_marks", "e5_answer", "e5_answer_total_marks", "e5_marks", "entity1", "entity2", "entity3", "entity4", "entity5", "marks", "question_id", "sub_question_description", "sub_question_id", "sub_question_number"]] = pd.DataFrame(data, index=df_questions.index)

                
            answers = st.session_state.db.child("student_answers").order_by_child("exam_id").equal_to(exam_id).get()
            ans_list = []
            for i, row in df_questions.iterrows():
                for ans in answers:
                    if ans.val()["sub_question_id"] == row['sub_question_id']:
                        ans_list.append([row['question_id'], ans.val()['sub_question_id'], ans.val()["student_id"], ans.val()["answer"], ans.val()["correct_keywords"], ans.val()["reference_keywords"], ans.val()["score"], ans.val()["verified"], row["topic"], row["total_marks"]])
            
            
            
                df_answers = pd.DataFrame(ans_list, columns = ['question_id', 'sub_question_id', 'student_id', 'answer', 'correct_keywords', 'reference_keywords', 'score', 'verified', 'topics', 'total_marks'])
                df_answers['student_id_int'] = df_answers['student_id'].astype(int)
                df_answers.sort_values(by=['student_id_int'], inplace=True)
                
                
            df_answers['question_description'] = ""
            df_answers = df_answers.set_index('question_id')
            df_questions = df_questions.set_index('question_id')
            df_answers.update(df_questions['question_description'])
            df_questions['question_id'] = df_questions.index
            df_answers['question_id'] = df_answers.index
            df_questions = df_questions.reset_index(drop=True)
            df_answers = df_answers.reset_index(drop=True)


        return df_questions, df_answers
    
    
    
    def get_student_answers(self, exam_id, df_questions):
        answers = st.session_state.db.child("student_answers").order_by_child("exam_id").equal_to(exam_id).get()
        ans_list = []
        for i, row in df_questions.iterrows():
            for i, sqid in enumerate(row['sub_question_id']):
                for ans in answers:
                    if ans.val()["sub_question_id"] == sqid:
                        ans_list.append([row['question_id'], ans.val()['sub_question_id'], ans.val()["student_id"], ans.val()["answer"], ans.val()["correct_keywords"], ans.val()["reference_keywords"], ans.val()["score"], ans.val()["verified"], row["topic"], row["total_marks"]])
        
        
        
                df_answers = pd.DataFrame(ans_list, columns = ['question_id', 'sub_question_id', 'student_id', 'answer', 'correct_keywords', 'reference_keywords', 'score', 'verified', 'topics', 'total_marks'])
                df_answers['student_id_int'] = df_answers['student_id'].astype(int)
                df_answers.sort_values(by=['student_id_int'], inplace=True)
                df_answers = df_answers.reset_index(drop=True)
                
        return df_answers
    
    
    
    def get_cut_off_conditions(self, df, col):
        cut_off_conds = [
            df[col] >= 85, 
            df[col] >= 80, 
            df[col] >= 75, 
            df[col] >= 70, 
            df[col] >= 65, 
            df[col] >= 60, 
            df[col] >= 55, 
            df[col] >= 50, 
            df[col] >= 40, 
            df[col] < 40, 
        ]
        
        return cut_off_conds
    
    
    
    def grade_conditions(self, df, col):
        grade_conds = [
            df[col] == "A+", 
            df[col] == "A", 
            df[col] == "A-", 
            df[col] == "B+", 
            df[col] == "B", 
            df[col] == "B-", 
            df[col] == "C+", 
            df[col] == "C", 
            df[col] == "D", 
            df[col] == "F", 
        ]
        
        return grade_conds
    
    
    
    def status_marks_conditions(self, df, col):
        status_marks_conds = [
            df[col] >= 50, 
            df[col] < 50
        ]
        
        return status_marks_conds
    
    
    
    def status_gp_conditions(self, df, col):
        status_gp_conds = [
            df[col] >= 2.00, 
            df[col] < 2.00
        ]
        
        return status_gp_conds
    
    
    def display_average_mark_speedometer(self, title, raw_mean_marks, full_marks):
        bar_color = ""
        bg_color = ""
        
        if raw_mean_marks / full_marks < 0.5:
            bar_color = "red"
            bg_color = "lightcoral"
        else:
            bar_color = "green"
            bg_color = "greenyellow"
            
        t = '<b>' + title + '<b>'
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = raw_mean_marks,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': t, 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [None, full_marks], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': bar_color},
                'bgcolor': bg_color,
                'borderwidth': 2,
                'bordercolor': "black",
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': full_marks/2}}
                    ))
    
        fig.update_layout( 
            font = {'color': bar_color, 'family': "Arial"},
            height=300, 
            )
    
        st.plotly_chart(fig, use_container_width=True)
        
        
    
    def display_marks_distribution(self, title, df):
        passing_mark = float(df.iloc[0]['total_marks']/2)
        df = pd.DataFrame(df['score'].value_counts())
        df.rename(columns={'score': 'num_of_stud'}, inplace=True, errors='raise')
        df = df.sort_index()
        df['score'] = df.index
        df['status']= df['score'].apply(lambda x: 'PASS' if (x >= passing_mark) else 'FAIL') 
    
        colors = {'PASS': 'green',
                  'FAIL': 'red'}
        
        bars = []
        for label, label_df in df.groupby('status'):
            bars.append(go.Bar(x=label_df.score,
                               y=label_df.num_of_stud,
                               name=label,
                               marker={'color': colors[label]}))
            
        # To swap elements so that pass marker comes first
        temp_bar = bars[0]
        bars[0] = bars[-1]
        bars[-1] = temp_bar
    
        t = '<b>' + title + '<b>'
        fig = go.FigureWidget(data=bars)
        fig.update_layout(
            title={
                'text': t,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(
                title="Score"
            ),
            yaxis=dict(
                title="Number of Students"
            ) 
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    def display_question_performance(self, title, df_answers):
        # Configuring a temp dataframe to plot the bar graph
        d = pd.DataFrame(df_answers.groupby(['sub_question_id'])['score'].mean())
        d['total_marks'] = pd.DataFrame(df_answers.groupby(['sub_question_id'])['total_marks'].mean())
        d['score_percentage'] = d['score'] / d['total_marks'] * 100
        d['status']= d['score_percentage'].apply(lambda x: 'PASS' if (x >= 50) else 'FAIL') 
        d['sub_question_id'] = d.index
        d = d.reset_index(drop=True)
        d['question_num'] = d.index + 1
    
        # Format to 2 decimal places
        d.style.format({
            'score': '{:,.2f}'.format,
            'total_marks': '{:,.2f}'.format,
            'score_percentage': '{:,.2f}'.format
        })
        
        colors = {'PASS': 'green', 'FAIL': 'red'}
    
        bars = []
        for label, label_df in d.groupby('status'):
            label_df.style.format({
                'score': '{:,.2f}'.format,
                'total_marks': '{:,.2f}'.format,
                'score_percentage': '{:,.2f}'.format
            })
    
            bars.append(go.Bar(x=label_df.question_num,
                               y=label_df.score_percentage,
                               name=label,
                               marker={'color': colors[label]}))
    
        # To swap elements so that pass marker comes first
        temp_bar = bars[0]
        bars[0] = bars[-1]
        bars[-1] = temp_bar
    
        t = '<b>' + title + '<b>'
        fig = go.FigureWidget(data=bars)
        fig.update_layout(
            title={
                'text': t,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(title="Question Number"),
            yaxis=dict(title="Percentage Score (%)") 
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    def get_students_results(self, df, grade_list, gp_list):
        exam_full_marks = df.groupby(['sub_question_id'])['total_marks'].mean().sum()
        df_results = pd.DataFrame(df.groupby(['student_id'])['score'].sum()/exam_full_marks*100)
        df_results["status"] = df_results['score'].apply(lambda x: 'PASS' if (x >= 50) else 'FAIL') 
        df_results['grade'] = np.select(self.get_cut_off_conditions(df_results, "score"), grade_list)
        df_results['grade_point'] = np.select(self.get_cut_off_conditions(df_results, "score"), gp_list)
        df_results['score'] = df_results['score'].round(2)
    
        return df_results, exam_full_marks
    
    
    
    def display_exam_stats(self, df):
        df_pass_rate = df.groupby(['status']).count()
        df_pass_rate.rename(columns={'score': 'num_of_stud'}, inplace=True, errors='raise')
        df_pass_rate['status'] = df_pass_rate.index
        number_of_candidates = int(df_pass_rate['num_of_stud'].sum())
        if len(df_pass_rate[df_pass_rate['status'] == "PASS"]['num_of_stud']) > 0:
            number_of_passes = int(df_pass_rate[df_pass_rate['status'] == "PASS"]['num_of_stud'])
            pass_rate = float(format(number_of_passes/number_of_candidates*100, ".2f"))
        else:
            number_of_passes = 0
            pass_rate = 0.00

        
        average_marks = float(format(df['score'].mean(), ".2f"))
        average_gp = float(format(df['grade_point'].mean(), ".2f"))
        
        return number_of_candidates, pass_rate, average_marks, average_gp
        
    
    
    def get_question_passing_rate(self, df_answers, sqid):
        passing_mark = df_answers.iloc[0]['total_marks']/2
        df = df_answers[df_answers['sub_question_id'] == sqid]
        df['status']= df['score'].apply(lambda x: 'PASS' if (x >= passing_mark) else 'FAIL') 
        d = pd.DataFrame(df.groupby(['status'])['score'].count())
        d.rename(columns={'score': 'count'}, inplace=True, errors='raise')
        d['status'] = d.index
        d.reset_index(drop=True, inplace=True)

        return int(d[d['status'] == "PASS"]['count'])/d['count'].sum()
    
        
        
    def display_grade_distribution(self, df, gp_list, grade_list, status_list):
        # Set a temp dataframe
        df_grad_dist = df.groupby(['grade']).count()
        df_grad_dist['grade'] = df_grad_dist.index
        df_grad_dist['grade_point'] = np.select(self.grade_conditions(df_grad_dist, "grade"), gp_list)
        df_grad_dist['status'] = np.select(self.status_gp_conditions(df_grad_dist, "grade_point"), status_list)
        df_grad_dist.sort_values(["grade_point"], ascending = False, inplace = True)
        df_grad_dist.rename(columns={'score': 'number_of_students'}, inplace=True, errors='raise')
        df_grad_dist.reset_index(drop=True, inplace=True)
        
        colors = {'PASS': 'green',
                  'FAIL': 'red'}
    
        bars = []
        for label, label_df in df_grad_dist.groupby('status'):
            bars.append(go.Bar(x=label_df.grade,
                               y=label_df.number_of_students,
                               name=label,
                               marker={'color': colors[label]},
    
                              ))
        # To swap elements so that pass marker comes first
        temp_bar = bars[0]
        bars[0] = bars[-1]
        bars[-1] = temp_bar
    
        fig = go.FigureWidget(data=bars)
        fig.update_layout(
            title={
                'text': "<b>Exam Grade Distribution<b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(
                title="Grade",
                categoryorder='array',
                categoryarray= grade_list
            ),
            yaxis=dict(
                title="Number of Students"
            )                 
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        
    def display_exam_passing_rate(df, grade_list):
        df_pass_rate = df.groupby(['status']).count()
        df_pass_rate.rename(columns={'score': 'num_of_stud'}, inplace=True, errors='raise')
        df_pass_rate['status'] = df_pass_rate.index
        
        pie = (go.Pie(
        labels=df_pass_rate['status'],
        values=df_pass_rate['num_of_stud'],
        marker={'colors': ['green' if x == "PASS" else 'red' for x in df_pass_rate['status']]}))
    
        fig = go.FigureWidget(data=pie)
        fig.update_layout(
            title={
                'text': "<b>Grade Distribution<b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(
                title="Grade",
                categoryorder='array',
                categoryarray= grade_list
            ),
            yaxis=dict(
                title="Number of Students"
            )                 
        )
       
        st.plotly_chart(fig, use_container_width=True)
        
        
        

    def display_students_question_performance(self, title, df):
        d = pd.DataFrame(df.groupby(['sub_question_id'])['score'].mean())
        d['total_marks'] = pd.DataFrame(df.groupby(['sub_question_id'])['total_marks'].mean())
        d['score_percentage'] = d['score'] / d['total_marks'] * 100
        d['status']= d['score_percentage'].apply(lambda x: 'PASS' if (x >= 50) else 'FAIL') 
        d['sub_question_id'] = d.index
        d = d.reset_index(drop=True)
        d['question_num'] = d.index + 1
    
        d.style.format({
            'score': '{:,.2f}'.format,
            'total_marks': '{:,.2f}'.format,
            'score_percentage': '{:,.2f}'.format
        })
        
        colors = {'PASS': 'green',
                  'FAIL': 'red'}
    
        bars = []
        for label, label_df in d.groupby('status'):
            label_df.style.format({
                'score': '{:,.2f}'.format,
                'total_marks': '{:,.2f}'.format,
                'score_percentage': '{:,.2f}'.format
            })
    
            bars.append(go.Bar(x=label_df.question_num,
                               y=label_df.score_percentage,
                               name=label,
                               marker={'color': colors[label]}))
    
        # To swap elements so that pass marker comes first
        temp_bar = bars[0]
        bars[0] = bars[-1]
        bars[-1] = temp_bar
    
        fig = go.FigureWidget(data=bars)
        fig.update_traces(marker_line_color = "black", marker_line_width = 1)
        fig.update_layout(
            title={
                'text': '<b>' + title + '<b>',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(
                title="Question Number"
            ),
            yaxis=dict(
                title="Percentage Score (%)"
            ) 
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        
 
    def send_feedback_email(self, studid_list, df_questions, df_answers, df_results):
        with st.form(key='send_email'):
            st.header("Email Exam Results to Students")
            chk_send_email = st.checkbox("I am sure I want to email exam results to all students.")
            btn_send = st.form_submit_button("Email Results")
        
        if btn_send and chk_send_email:
            for studid in studid_list:
                df_temp = df_answers[df_answers['student_id'] == studid]
                df_temp = df_temp.set_index('sub_question_id')
                df_temp = df_temp.reindex(index=df_questions['sub_question_id'])
                df_temp = df_temp.reset_index()
                
                attr = ["e1_answer", "e1_answer_total_marks", "e1_marks", "e2_answer", "e2_answer_total_marks", "e2_marks", "e3_answer", "e3_answer_total_marks", "e3_marks", "e4_answer", "e4_answer_total_marks", "e4_marks", "e5_answer", "e5_answer_total_marks", "e5_marks", "entity1", "entity2", "entity3", "entity4", "entity5", "marks", "question_id", "sub_question_description", "sub_question_id", "sub_question_number"]
                
                for a in attr:
                    df_temp[a] = np.where(df_temp['sub_question_id'] == df_questions['sub_question_id'], df_questions[a], "")
                    
                    
            #option = st.selectbox("Select a student to preview email", studid_list)
            #if any(option in i for i in studid_list):
            for studid in studid_list:
                marks = "{:.2f}".format(df_results[df_results.index == studid]['score'][0])
                grade = df_results[df_results.index == studid]['grade'][0]
                status = df_results[df_results.index == studid]['status'][0]
                
                website_email = 'automated.exam.marking.system@gmail.com'
                body_message_list = [
                    'Dear Student (Student ID: ', studid, '),\n\n',
                    'Please find your results of the ', st.session_state.view_this_exam.iloc[0]['exam_title'], ' as follows:',
                    '\n\nMarks: ', str(marks), ' %',
                    '\nGrade: ', grade, ' (', status, ')', 
                    '\n\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n',
                    '\nThe answers of the questions can be found below: \n'
                ]
                
                for i, row in df_questions.iterrows():
                    body_message_list.append('...........................................................................................................................................................................................................\n')
                    body_message_list.append('Question ' + str(i + 1) + ' ' + row['question_description'] + '\n\n')
                    body_message_list.append(row['entity1'] + '\n' + row['e1_answer'] + '\n\n')
    
                    
                    if not row['e2_answer'] == '':
                        body_message_list.append(row['entity2'] + '\n' + row['e2_answer'] + '\n\n')
                        
                    if not row['e3_answer'] == '':
                        body_message_list.append(row['entity3'] + '\n' + row['e3_answer'] + '\n\n')
                        
                    if not row['e4_answer'] == '':
                        body_message_list.append(row['entity4'] + '\n' + row['e4_answer'] + '\n\n')
                        
                    if not row['e5_answer'] == '':
                        body_message_list.append(row['entity5'] + '\n' + row['e5_answer'] + '\n\n')
                        
                    
                        
                body_message_list.append('\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                body_message_list.append("\nThese are your answers and scores: \n")
                
                for i, row in df_temp.iterrows():
                    body_message_list.append('...........................................................................................................................................................................................................\n')
                    body_message_list.append("Question " + str(i + 1))
                    body_message_list.append("\n\nYour Answer: " + row['answer'])
                    body_message_list.append("\n\nScore: " + str(row['score']) + '/' + str(row['total_marks']) + '\n')
                    
                    
                body_message_list.append('\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                body_message_list.append('\nPlease do not reply to this email as it is autogenerated by the system.')
                
                
            
            
                website_email = 'automated.exam.marking.system@gmail.com'
                email_password = 'isajaoxknpcsvygq'
                sub = st.session_state.view_this_exam.iloc[0]['exam_title'] + ' Result'
                body_message = ''.join(str(b) for b in body_message_list)
                emails = studid + '@kdu-online.com'
                
                sent_from = website_email
                to = emails
                subject = sub
                body = body_message
            
                email_text = 'Subject: {}\n\n{}'.format(subject, body).encode('utf-8')
                
                try:
                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtp_server.ehlo()
                    smtp_server.login(website_email, email_password)
                    smtp_server.sendmail(sent_from, to, email_text)
                    smtp_server.close()
                    st.success("Email sent successfully!")
                except Exception as ex:
                    st.error("Something went wrong…." + str(ex))
        