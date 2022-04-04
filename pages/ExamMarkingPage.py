# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 20:59:21 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp
import pandas as pd
from annotated_text import annotated_text
from PIL import Image

import re
import nltk
from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('english')




from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer



class ExamMarkingPage(HydraHeadApp):    
    def run(self):
        # Save variables into session state
        if 'mark_this_exam' not in st.session_state:
            st.session_state.mark_this_exam = ''
            
        if 'df_questions' not in st.session_state:
            st.session_state.df_question = None
            
        if 'question' not in st.session_state:
            st.session_state.question = None
            
        if 'df_answers' not in st.session_state:
            st.session_state.df_answers = None
            
        if 'sub_question_id' not in st.session_state:
            st.session_state.sub_question_id = ''
            


        line = '''
        ---
        '''
            
        # Set option tuple (all exams loaded)
        option_tuple = self.get_exam_data()  
        option = st.sidebar.selectbox("Select an Exam", option_tuple, on_change = self.reset)
    
            
        # Dashboard page
        if option == option_tuple[0]:
            st.markdown("<h1 style='text-align: center; line-height: 120px;'>Exam Marking Page</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; line-height: 120px;'>Select an Exam Title on the sidebar</h3>", unsafe_allow_html=True)
            image = "https://raw.githubusercontent.com/junchao1507/FYP-Implementation/main/images/ComputerGrading4.jpg"
            st.image(image, caption='', width=1450)
            
        # Specific exam oage
        elif any(option in i for i in option_tuple):
            # Get the current exam and save it into a variable
            st.session_state.mark_this_exam = st.session_state.exams.loc[(st.session_state.exams['exam_title'] == option) &
                                                   (st.session_state.exams['user_id'] == st.session_state.current_user['user_id'])]
        
            # Display the exam title
            st.title(st.session_state.mark_this_exam.iloc[0]['exam_title'])
            
            col1, col2 = st.columns(2)
            original_keywords = []
            extended_keywords = []
            entity_names = []
            subques_marks = []
            ans_total_marks = []
            
            with col1:
                # Get exam questions for this exam
                st.session_state.df_questions = self.get_questions(st.session_state.current_user['user_id'], st.session_state.mark_this_exam.iloc[0]['exam_id'])
                # Set the question typle (load all exam questions)
                ques_tuple = [ "Question " + str(i + 1) for i in range(len(st.session_state.df_questions))]
                st.session_state.question = st.selectbox("Select Exam Question", (ques_tuple), on_change = self.reset)
                    
                # Display exam information
                with st.form(key = st.session_state.question + 'display'):
                    markdown = "**" + st.session_state.question + "**"
                    st.header(markdown)
                    st.markdown("**Question Description:** " + st.session_state.df_questions.iloc[int(st.session_state.question[-1]) - 1]['question_description'])
                    st.markdown("**Question Total Marks:** " + str(st.session_state.df_questions.iloc[int(st.session_state.question[-1]) - 1]['total_marks']))
                    st.write(line)
                    st.write('\n')
                    
                    
                        
                    subquestion = st.session_state.db.child("saq_sub_questions").order_by_child("question_id").equal_to(st.session_state.df_questions.iloc[int(st.session_state.question[-1]) - 1]['question_id']).get()

                    # Get sample answers from subquestions.
                    for s in subquestion.each():
                        st.session_state.sub_question_id = s.val()['sub_question_id']
                        #st.write(st.session_state.sub_question_id)
                        
                        original_keywords.append(self.preprocess_sent(s.val()['e1_answer']))
                        extended_keywords.append(self.expand_keywords(self.preprocess_sent(s.val()['e1_answer'])))
                        entity_names.append(s.val()['entity1'])
                        subques_marks.append(s.val()['e1_marks'])
                        ans_total_marks.append(s.val()['e1_answer_total_marks'])
                        st.markdown("**Entity 1:** " + s.val()['entity1'])
                        st.markdown("**Entity 1 Marks Allocated:** " + str(s.val()['e1_marks']))
                        st.markdown("**Entity 1 Answer:** " + s.val()['e1_answer'])
                        st.markdown("**Entity 1 Answer Keywords:** ",)
                        st.markdown(self.preprocess_sent(s.val()['e1_answer']))
                        st.markdown("**Entity 1 Answer Total Marks:** " + str(s.val()['e1_answer_total_marks']))
                        st.write(line)
                        st.write('\n')
                        
                        if s.val()['e2_answer']:
                            original_keywords.append(self.preprocess_sent(s.val()['e2_answer']))
                            extended_keywords.append(self.expand_keywords(self.preprocess_sent(s.val()['e2_answer'])))
                            entity_names.append(s.val()['entity2'])
                            subques_marks.append(s.val()['e2_marks'])
                            ans_total_marks.append(s.val()['e2_answer_total_marks'])
                            st.markdown("**Entity 2:** " + s.val()['entity2'])
                            st.markdown("**Entity 2 Marks Allocated:** " + str(s.val()['e2_marks']))
                            st.markdown("**Entity 2 Answer:** " + s.val()['e2_answer'])
                            st.markdown("**Entity 2 Answer Keywords:** ",)
                            st.markdown(self.preprocess_sent(s.val()['e2_answer']))
                            st.markdown("**Entity 2 Answer Total Marks:** " + str(s.val()['e2_answer_total_marks']))
                            st.write(line)
                            st.write('\n')
                            
                        if s.val()['e3_answer']:
                            original_keywords.append(self.preprocess_sent(s.val()['e3_answer']))
                            extended_keywords.append(self.expand_keywords(self.preprocess_sent(s.val()['e3_answer'])))
                            entity_names.append(s.val()['entity3'])
                            subques_marks.append(s.val()['e3_marks'])
                            ans_total_marks.append(s.val()['e3_answer_total_marks'])
                            st.markdown("**Entity 3:** " + s.val()['entity3'])
                            st.markdown("**Entity 3 Marks Allocated:** " + str(s.val()['e3_marks']))
                            st.markdown("**Entity 3 Answer:** " + s.val()['e3_answer'])
                            st.markdown("**Entity 3 Answer Keywords:** ",)
                            st.markdown(self.preprocess_sent(s.val()['e3_answer']))
                            st.markdown("**Entity 3 Answer Total Marks:** " + str(s.val()['e3_answer_total_marks']))
                            st.write(line)
                            st.write('\n')
                            
                        if s.val()['e4_answer']:
                            original_keywords.append(self.preprocess_sent(s.val()['e4_answer']))
                            extended_keywords.append(self.expand_keywords(self.preprocess_sent(s.val()['e4_answer'])))
                            entity_names.append(s.val()['entity4'])
                            subques_marks.append(s.val()['e4_marks'])
                            ans_total_marks.append(s.val()['e4_answer_total_marks'])
                            st.markdown("**Entity 4:** " + s.val()['entity4'])
                            st.markdown("**Entity 4 Marks Allocated:** " + str(s.val()['e4_marks']))
                            st.markdown("**Entity 4 Answer:** " + s.val()['e4_answer'])
                            st.markdown("**Entity 4 Answer Keywords:** ",)
                            st.markdown(self.preprocess_sent(s.val()['e4_answer']))
                            st.markdown("**Entity 4 Answer Total Marks:** " + str(s.val()['e4_answer_total_marks']))
                            st.write(line)
                            st.write('\n')
                            
                        if s.val()['e5_answer']:
                            original_keywords.append(self.preprocess_sent(s.val()['e5_answer']))
                            extended_keywords.append(self.expand_keywords(self.preprocess_sent(s.val()['e5_answer'])))
                            entity_names.append(s.val()['entity5'])
                            subques_marks.append(s.val()['e5_marks'])
                            ans_total_marks.append(s.val()['e5_answer_total_marks'])
                            st.markdown("**Entity 5:** " + s.val()['entity5'])
                            st.markdown("**Entity 5 Marks Allocated:** " + str(s.val()['e5_marks']))
                            st.markdown("**Entity 5 Answer:** " + s.val()['e5_answer'])
                            st.markdown("**Entity 5 Answer Keywords:** ",)
                            st.markdown(self.preprocess_sent(s.val()['e5_answer']))
                            st.markdown("**Entity 5 Answer Total Marks:** " + str(s.val()['e5_answer_total_marks']))
                            st.write(line)
                            st.write('\n')

                        
                    st.checkbox("Edit", key = "chk_edit")
                    
                    btn_edit_answer = st.form_submit_button("Edit Answer")
                
                if st.session_state.chk_edit:
                    self.edit_answer()
                        
            with col2:
                student_answers = st.session_state.db.child("student_answers").order_by_child("exam_id").equal_to(st.session_state.mark_this_exam.iloc[0]['exam_id']).get()
                st.session_state.df_answers = pd.DataFrame(columns = ['sub_question_id', 'student_id', 'answer', 'correct_keywords', 'reference_keywords', 'score', 'verified'])
                
                answers = []
                for ans in student_answers.each():
                    if ans.val()['sub_question_id'] == st.session_state.sub_question_id:
                        answers.append([ans.val()['sub_question_id'], ans.val()["student_id"], ans.val()["answer"], ans.val()["correct_keywords"], ans.val()["reference_keywords"], ans.val()["score"], ans.val()["verified"]])
                    
                st.session_state.df_answers = pd.DataFrame(answers, columns = ['sub_question_id', 'student_id', 'answer', 'correct_keywords', 'reference_keywords', 'score', 'verified'])
                
                st.session_state.df_answers['student_id_int'] = st.session_state.df_answers['student_id'].astype(int)
                st.session_state.df_answers.sort_values(by=['student_id_int'], inplace=True)
                st.session_state.df_answers = st.session_state.df_answers.reset_index(drop=True)
                
                #st.write(st.session_state.df_answers)
                
                if not st.session_state.df_answers.empty:
                    if "i" not in st.session_state:
                        st.session_state.i = 0
                        
                    if "verified" not in st.session_state:
                        st.session_state.verified = 0
                        
                    if st.session_state.i > 0:
                        btn_prev = st.button("<< Prev Student (" + st.session_state.df_answers.iloc[st.session_state.i - 1]['student_id'] + ")", on_click=self.decrement)
    
    
                    student_ans = st.session_state.df_answers.iloc[st.session_state.i]['answer']
                    st.session_state.verified  = st.session_state.df_answers.iloc[st.session_state.i]['verified']
                    color_list = ['#00818A', '#7045AF', '#00818A', '#7045AF', '#00818A', '#7045AF', '#00818A', '#7045AF', '#00818A', '#7045AF']
                    score = 0
                    total_score = 0
                    correct_keys = []
                    reference_keys = []
    
                    with st.form(key='marking_form' + st.session_state.df_answers.iloc[st.session_state.i]['student_id']):
                        st.title('**Marking Form**')
                        
                        if st.session_state.verified == 0:
                            st.warning("Marks have not been saved into the database")
                            
                        else:
                            st.success("Marks have been saved into the database, you may update the marks.")
                        
                        id_md = "**Student ID:** " + st.session_state.df_answers.iloc[st.session_state.i]['student_id']
                        st.markdown(id_md)
                        st.session_state.verified = st.session_state.df_answers.iloc[st.session_state.i]['verified']
                        st.markdown("**Original Answer:** " + student_ans)
                        st.write(line)

                        
                        for j, (original_keyword_lists, extended_keyword_lists, entity_name, subques_mark, ans_total_mark) in enumerate(zip(original_keywords, extended_keywords, entity_names, subques_marks, ans_total_marks)):
                            st.write('\n')
                            md = '**Entity Name: ' + entity_name + '**'
                            st.markdown(md)
                            st.markdown("***Keywords from Stdent's Answer:***")
                            prepros_sent = self.preprocess_sent(student_ans)
                            highlight_text, cor_keys, ref_keys = self.set_highlight_keywords(prepros_sent, extended_keyword_lists, color_list[j * 2 : j * 2 + 2])
                            correct_keys.append(cor_keys)
                            reference_keys.append(ref_keys)
                            annotated_text(*highlight_text)
                            st.write()
                            
                            cos_sim = self.cal_cos_similarity(' '.join(original_keyword_lists), ' '.join(cor_keys))
                            score = self.cal_entity_score(cos_sim, subques_mark, ans_total_mark)
                            total_score += score
                            st.write('\n')
                            st.markdown('***Cosine Similarity:*** ' + str(cos_sim))
                            st.markdown('***Predicted score:*** ' + str(score))
                            st.write(line)
                            
                        st.markdown('**Total Predicted Score:** ' + str(total_score))
                        st.number_input('Finalized Score: ', value = total_score)
                        
                        button_display = ""
                        if st.session_state.verified == 1:
                            button_display = "Resubmit Score"
                        else:
                            button_display = "Submit Score"
                            
                        btn_submit = st.form_submit_button(button_display)
                        
                    if btn_submit:

                        st.session_state.df_answers.at[st.session_state.i,'correct_keywords'] = correct_keys
                        st.session_state.df_answers.at[st.session_state.i, 'reference_keywords'] = reference_keys
                        st.session_state.df_answers["score"] = st.session_state.df_answers["score"].astype(float)
                        st.session_state.df_answers.at[st.session_state.i, 'score'] = total_score
                        st.session_state.df_answers["verified"] = st.session_state.df_answers["verified"].astype(int)
                        st.session_state.df_answers.at[st.session_state.i, 'verified'] = 1


                        answer_dict = {
                            "answer" : st.session_state.df_answers.iloc[st.session_state.i]['answer'],
                            "correct_keywords" : st.session_state.df_answers.iloc[st.session_state.i]['correct_keywords'],
                            "exam_id" : st.session_state.mark_this_exam.iloc[0]['exam_id'],
                            "reference_keywords" : st.session_state.df_answers.iloc[st.session_state.i]['reference_keywords'],
                            "score" : st.session_state.df_answers.iloc[st.session_state.i]['score'],
                            "student_id" : st.session_state.df_answers.iloc[st.session_state.i]['student_id'],
                            "sub_question_id" : st.session_state.df_answers.iloc[st.session_state.i]['sub_question_id'],
                            "verified" : int(st.session_state.df_answers.iloc[st.session_state.i]['verified']),
                        }
                        
                        student_answers = st.session_state.db.child("student_answers").order_by_child("student_id").equal_to(st.session_state.df_answers.iloc[st.session_state.i]['student_id']).get()
                        
                        ans_id = ""
                        for stud_ans in student_answers.each():
                            if stud_ans.val()['sub_question_id'] == st.session_state.df_answers.iloc[st.session_state.i]['sub_question_id']:
                                ans_id = stud_ans.key()
                        
                        st.session_state.db.child("student_answers").child(ans_id).update(answer_dict)
                        st.success("Score submitted successfully!")
                        st.session_state.verified = 1
                            
                        btn_refresh = st.button('Refresh Page')
                    
                    if len(st.session_state.df_answers) > 1 and len(st.session_state.df_answers) > st.session_state.i + 1:
                        btn_next = st.button("Next Student >> (" + st.session_state.df_answers.iloc[st.session_state.i + 1]['student_id'] + ")", on_click=self.increment)
                else:
                    st.warning('No answer found.')
                    st.warning('Want to held an examination? Go to the Exam dahsboard page to send email to your students.')
            
            
    def increment(self):
        st.session_state.i += 1
        
        
    def decrement(self):
        st.session_state.i -= 1
        
    
    def reset(self):
        st.session_state.i = 0
        st.session_state.verified = 0
            
            
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
    
    
    
    def get_questions(self, user_id, exam_id):
        # Check if there's exam records in the firebase
        if st.session_state.db.child('exams').shallow().get().val():
            exams_dict = st.session_state.db.child("exams").order_by_child("timestamp_created").order_by_child("user_id").equal_to(user_id).get()
    
        questions = []
        
        # Loop through each exam records and extend the question_ids to the questions list
        for e in exams_dict.each():
            if e.val()['exam_id'] == exam_id:
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
                
        return temp_question
    
    
    
    def preprocess_sent(self, sent):
        # Setting up punctuations to be replaced (Punctuations, Tags, Symbols) using regular expression
        REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})|(\&)")
        REPLACE_WITH_SPACE = re.compile("(<br\s/><br\s/?)|(-)|(/)|(:).")
        
    
        temp1 = sent
    
        # Remove puctuation & convert all text to lower cases
        temp1 = REPLACE_NO_SPACE.sub("", temp1.lower())
        temp1 = REPLACE_WITH_SPACE.sub(" ", temp1)
    
        # Tokenization
        temp2 = nltk.word_tokenize(temp1)
    
        # Remove stop words but keep negation words
        negations = {'no', 'nor', 'not', 'don', "don't",'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
        stopwords = set(stop_words)
        customized_stopwords = stopwords - negations
        temp2 = [word for word in temp2 if not word in customized_stopwords]
        
        # Lemmatization (remove ing, s,etc.)
        temp3=''
        for word in temp2:
            temp3 = temp3 + ' ' + str(lemmatizer.lemmatize(word))
            
        return temp3.strip().split()



    def expand_keywords(self, word_list):
        syn = []
        
        # Loop through every word in the current line of text
        for word in word_list:
            synonyms = wn.synsets(word)
            temp_syn = []
            
            if len(synonyms) > 0:
                #syn.append([word])
                temp_syn.append(word)
                for ss in synonyms:
                    for s in ss.lemma_names():
                        if s not in temp_syn:
                            temp_syn.append(s.replace('_',' '))    
                syn.append(temp_syn)

        return syn
    
    
    
    def set_highlight_keywords(self, process_ans_list, keywords_list, color_list):
        highlight_keywords = []
        correct_keywords = []
        reference_keywords = []
        keyword = False
        
        # Iterate through the student's answer keyword list
        for ans in process_ans_list:
            keyword = False
            color = ""
            key_type = ""
            
            # Iterate through the keyword list based on the original keyword
            for kw in keywords_list:
                if not keyword:
                    # Iterate through tge keyword lists
                    for i, k in enumerate(kw):
                        # If index = 0 , set the keyword as the actual keyword
                        if i == 0:
                            actual_keyword = k
                            # If keyword is found, append keyword and actual keywords
                        if ans == k:
                            keyword = True
                            reference_keywords.append(ans)
                            correct_keywords.append(actual_keyword)
                            
                            # If the keyword index is 0, label it as the actual keyword
                            # Else, label as synonym keyword
                            if i == 0:
                                color = color_list[0]
                                key_type = "actual keyword"
                            else:
                                color = color_list[1]
                                key_type = "synonym keyword"

            app = None
            # Set the answer text to be highlighted as well as the highlight labels.
            if keyword:
                app = (ans + ' ', key_type, color)
            else:
                app = ans + ' '

            highlight_keywords.append(app)
            keyword = False
        
        # Append empty string if no keyword is found.
        if len(correct_keywords) == 0:
            correct_keywords.append("")
        
        if len(reference_keywords) == 0:
            reference_keywords.append("")
        
        return highlight_keywords, correct_keywords, reference_keywords
    
    
    
    def cal_cos_similarity(self, sample_answer, student_answer):
        data = [sample_answer, student_answer]
        count_vectorizer = CountVectorizer()
        vector_matrix = count_vectorizer.fit_transform(data)
        tokens = count_vectorizer.get_feature_names()
        vector_matrix.toarray()
        cosine_similarity_matrix = cosine_similarity(vector_matrix)
        cos_similarity = cosine_similarity_matrix[0][1]
        
        return cos_similarity
    
    
    
    def det_score(self, decimal, score, ques_score):
        if score >= ques_score:
            score = ques_score
        elif decimal < 0.01:
            score = int(score)
        elif decimal >= 0.01 and decimal < 0.25:
            score = int(score) + 0.25
        elif decimal >= 0.25 and decimal < 0.5:
            score = int(score) + 0.5
        elif decimal >= 0.5 and decimal < 0.75:
            score = int(score) + 0.75
        elif decimal > 0.75:
            score = int(score) + 1
            
        return score
    
    
    
    def cal_entity_score(self, cos_sim, ques_score, ans_total_score):
        score = cos_sim * ques_score * (ans_total_score / ques_score)
        decimal = score - int(score)
        score = self.det_score(decimal, score, ques_score)
        
        return score
    
    
    
    def upload_marks(self, index, correct_keywords, reference_keywords, total_score):
        pass
        
    

    
    def edit_answer(self):
        with st.form(key = st.session_state.question + 'edit'):
            markdown = "**Edit " + st.session_state.question + "**"
            st.header(markdown)

            subquestion = st.session_state.db.child("saq_sub_questions").order_by_child("question_id").equal_to(st.session_state.df_questions.iloc[int(st.session_state.question[-1])-1]['question_id']).get()

            saq_id = ''
            for s in subquestion.each():
                saq_id = s.val()['sub_question_id']
                
                st.text_input("Entity 1: ", value = s.val()['entity1'], key = "entity1")
                st.number_input("Entity 1 Marks Allocated: ", value = s.val()['e1_marks'], min_value = 1, step = 1, key = "e1_marks")
                st.text_area("Entity 1 Answer: ", value = s.val()['e1_answer'], key = "e1_answer")
                st.number_input("Entity 1 Answer Total Marks:: ", value = s.val()['e1_answer_total_marks'], min_value = 1, step = 1, key = "e1_answer_total_marks")

                
                if s.val()['e2_answer']:
                    st.text_input("Entity 2: ", value = s.val()['entity2'], key = "entity2")
                    st.number_input("Entity 2 Marks Allocated: ", value = s.val()['e2_marks'], min_value = 1, step = 1, key = "e2_marks")
                    st.text_area("Entity 2 Answer: ", value = s.val()['e2_answer'], key = "e2_answer")
                    st.number_input("Entity 2 Answer Total Marks:: ", value = s.val()['e2_answer_total_marks'], min_value = 1, step = 1, key = "e2_answer_total_marks")
                    
                if s.val()['e3_answer']:
                    st.text_input("Entity 3: ", value = s.val()['entity3'], key = "entity3")
                    st.number_input("Entity 3 Marks Allocated: ", value = s.val()['e3_marks'], min_value = 1, step = 1, key = "e3_marks")
                    st.text_area("Entity 3 Answer: ", value = s.val()['e3_answer'], key = "e3_answer")
                    st.number_input("Entity 3 Answer Total Marks:: ", value = s.val()['e3_answer_total_marks'], min_value = 1, step = 1, key = "e3_answer_total_marks")
                    
                if s.val()['e4_answer']:
                    st.text_input("Entity 4: ", value = s.val()['entity4'], key = "entity4")
                    st.number_input("Entity 4 Marks Allocated: ", value = s.val()['e4_marks'], min_value = 1, step = 1, key = "e4_marks")
                    st.text_area("Entity 4 Answer: ", value = s.val()['e4_answer'], key = "e4_answer")
                    st.number_input("Entity 4 Answer Total Marks:: ", value = s.val()['e4_answer_total_marks'], min_value = 1, step = 1, key = "e4_answer_total_marks")
                    
                if s.val()['e5_answer']:
                    st.text_input("Entity 5: ", value = s.val()['entity5'], key = "entity5")
                    st.number_input("Entity 5 Marks Allocated: ", value = s.val()['e5_marks'], min_value = 1, step = 1, key = "e5_marks")
                    st.text_area("Entity 5 Answer: ", value = s.val()['e5_answer'], key = "e5_answer")
                    st.number_input("Entity 5 Answer Total Marks:: ", value = s.val()['e5_answer_total_marks'], min_value = 1, step = 1, key = "e5_answer_total_marks")

            
            
            btn_proceed = st.form_submit_button("Proceed")
            
        if btn_proceed:
            saq={
                'entity1' : st.session_state.entity1,
                'e1_marks': st.session_state.e1_marks,
                'e1_answer' : st.session_state.e1_answer,
                'e1_answer_total_marks' : st.session_state.e1_answer_total_marks,
                
                'entity2' : st.session_state.entity2,
                'e2_marks': st.session_state.e2_marks,
                'e2_answer' : st.session_state.e2_answer,
                'e2_answer_total_marks' : st.session_state.e2_answer_total_marks,
                
                'entity3' : st.session_state.entity3,
                'e3_marks': st.session_state.e3_marks,
                'e3_answer' : st.session_state.e3_answer,
                'e3_answer_total_marks' : st.session_state.e3_answer_total_marks,
                
                'entity4' : st.session_state.entity4,
                'e4_marks': st.session_state.e4_marks,
                'e4_answer' : st.session_state.e4_answer,
                'e4_answer_total_marks' : st.session_state.e4_answer_total_marks,
                
                'entity5' : st.session_state.entity5,
                'e5_marks': st.session_state.e5_marks,
                'e5_answer' : st.session_state.e5_answer,
                'e5_answer_total_marks' : st.session_state.e5_answer_total_marks
                }
            
            st.session_state.db.child("saq_sub_questions").child(saq_id).update(saq)
            st.success('Updated Successfully.')
            btn_done = st.button('Refresh Page', on_click = self.reset_chk_edit)
            
            
    def reset_chk_edit(self):
        st.session_state.chk_edit = False