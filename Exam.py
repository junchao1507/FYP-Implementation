# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:41:56 2022

@author: Lenovo
"""

class Exam:
    def __init__(self, exam_id, exam_password, exam_title, num_of_ques, total_marks, duration_minutes, start_time, timestamp_created, user_id):
        self.exam_id = exam_id
        self.exam_password = exam_password
        self.exam_title = exam_title
        self.num_of_ques = num_of_ques
        self.total_marks = total_marks
        self.duration_minutes = duration_minutes
        self.start_time = start_time
        self.timestamp_created = timestamp_created
        self.user_id = user_id
        
# =============================================================================
#     def create_exam(self, exam_id, exam_password, exam_title, num_of_ques, total_marks, duration_minutes, start_time, user_id):
#         self.exam_id = exam_id
#         self.exam_password = exam_password
#         self.exam_title = exam_title
#         self.num_of_ques = num_of_ques
#         self.total_marks = total_marks
#         self.duration_minutes = duration_minutes
#         self.start_time = start_time
# =============================================================================
        
    def set_exam_id(self, exam_id):
        self.exam_id = exam_id
        
    def set_exam_password(self, exam_password):
        self.exam_password = exam_password
        
    def set_exam_title(self, exam_title):
        self.exam_title = exam_title
        
    def set_num_of_ques(self, num_of_ques):
        self.num_of_ques = num_of_ques
        
    def set_total_marks(self, total_marks):
        self.total_marks = total_marks
        
    def set_duration_minutes(self, duration_minutes):
        self.duration_minutes = duration_minutes
        
    def set_timestamp_created(self, timestamp_created):
        self.timestamp_created = timestamp_created
        
    def set_start_time(self, start_time):
        self.start_time = start_time
        
    def get_exam_id(self):
        return self.exam_id
    
    def get_exam_password(self):
        return self.exam_password
    
    def get_exam_title(self):
        return self.exam_title 
        
    def get_num_of_ques(self):
        return self.num_of_ques
        
    def get_total_marks(self):
        return self.total_marks
        
    def get_duration_minutes(self):
        return self.duration_minutes
    
    def get_timestamp_created(self):
        return self.timestamp_created
        
    def get_start_time(self):
        return self.start_time 
        
        
class Question:
    def _init_(self):
        self.q_id = None
        self.q_desciption = None
        self.topic = None
        self.total_marks = None
        self.exam_id = None
        
    def create_question(self, q_id, q_desciption, topic, total_marks, exam_id):
        self.q_id = q_id
        self.q_desciption = q_desciption
        self.topic = topic
        self.total_marks = total_marks
        self.exam_id = exam_id
        
    def set_q_id(self, q_id):
        self.q_id = q_id
        
    def set_q_description(self, q_desciption):
        self.q_desciption = q_desciption
        
    def set_topic(self, topic):
         self.topic = topic
        
    def set_total_marks(self, total_marks):
        self.total_marks = total_marks
        
    def set_exam_id(self, exam_id):
        self.exam_id = exam_id
        
    def get_q_id(self):
        return self.q_id
        
    def get_q_description(self):
        return self.q_desciption
        
    def get_topic(self):
        return self.topic 
        
    def get_total_marks(self):
        return self.total_marks 
        
    def get_exam_id(self):
        return self.exam_id 
        

class MultipleChoiceQuestion(Question):
    def _init_(self):
        super().__init__(self)
        self.subques_id = None
        self.subques_description = None
        self.subques_marks = None
        self.opt_a = None
        self.opt_b = None
        self.opt_c = None
        self.opt_d = None
        self.answer = None
        
    def create_mcq(self, q_id, q_desciption, topic, total_marks, exam_id, subques_id, subques_description, subques_marks, opt_a, opt_b, opt_c, opt_d, answer):
        Question.create_question(self, q_id, "MCQ", q_desciption, topic, total_marks, exam_id)
        self.subques_id = subques_id #(a, b, c, ... )
        self.subques_description = subques_description
        self.subques_marks = subques_marks
        self.opt_a = opt_a
        self.opt_b = opt_b
        self.opt_c = opt_c
        self.opt_d = opt_d
        self.answer = answer

    def set_q_id(self, q_id):
        Question.set_q_id(q_id)
        
    def set_q_type(self):
        Question.set_q_type("MCQ")
        
    def set_q_description(self, q_description):
        Question.set_q_description(q_description)
        
    def set_topic(self, topic):
        Question.set_topic(topic)
        
    def set_total_marks(self, total_marks):
        Question.set_total_marks(total_marks)
        
    def set_exam_id(self, exam_id):
        Question.set_exam_id(exam_id)

    def set_subques_id(self, subques_id):
        self.subques_id = subques_id
        
    def set_subques_marks(self, subques_marks):
        self.subques_marks = subques_marks
        
    def set_opt_a(self, opt_a):
        self.opt_a = opt_a
        
    def set_opt_b(self, opt_b):
        self.opt_b = opt_b
        
    def set_opt_c(self, opt_c):
        self.opt_c = opt_c
        
    def set_opt_d(self, opt_d):
        self.opt_d = opt_d
        
    def set_answer(self, answer):
        self.answer = answer

    def get_q_id(self):
        return Question.get_q_id(self)
        
    def get_q_type(self):
        return Question.get_q_type(self)
        
    def get_q_description(self):
        return Question.get_q_description(self)
        
    def get_topic(self):
        return Question.get_topic(self)
        
    def get_total_marks(self):
        return Question.get_total_marks(self)
        
    def get_exam_id(self):
        return Question.get_exam_id(self)
    
    def get_subques_id(self):
        return self.subques_id
        
    def get_subques_marks(self):
        return self.subques_marks
        
    def get_opt_a(self):
        return self.opt_a
        
    def get_opt_b(self):
        return self.opt_b
        
    def get_opt_c(self):
        return self.opt_c
        
    def get_opt_d(self):
        return self.opt_d
        
    def get_answer(self):
        return self.answer
        
        
class SingleEntityQuestion(Question):
    def _init_(self):
        super().__init__(self)
        self.subques_id = None
        self.subques_description = None
        self.subques_total_marks = None
        self.subques_keywords = None
        self.subques_answer = None 
        
    def create_single_entity_saq(self, q_id, q_desciption, topic, total_marks, exam_id, subques_id, subques_description, subques_total_marks, subques_keywords, subques_answer):
        Question.create_question(self, q_id, "Single Entity OEQ", q_desciption, topic, total_marks, exam_id)
        self.subques_id = subques_id
        self.subques_description = subques_description
        self.subques_total_marks = subques_total_marks
        self.subques_keywords = subques_keywords
        self.subques_answer = subques_answer 
        
    def set_q_id(self, q_id):
        Question.set_q_id(q_id)
        
    def set_q_type(self):
        Question.set_q_type("Single Entity OEQ")
        
    def set_q_description(self, q_description):
        Question.set_q_description(q_description)
        
    def set_topic(self, topic):
        Question.set_topic(topic)
        
    def set_total_marks(self, total_marks):
        Question.set_total_marks(total_marks)
        
    def set_exam_id(self, exam_id):
        Question.set_exam_id(exam_id)
        
    def set_subques_id(self, subques_id):
        self.subques_id = subques_id
        
    def set_subques_description(self, subques_description):
        self.subques_description = subques_description
        
    def set_subques_total_marks(self, subques_total_marks):
        self.subques_total_marks = subques_total_marks 
        
    def set_subques_keywords(self, subques_keywords):
        self.subques_keywords = subques_keywords
        
    def set_subques_answer(self, subques_answer):
        self.subques_answer = subques_answer
        
    def get_q_id(self):
        return Question.get_q_id(self)
        
    def get_q_type(self):
        return Question.get_q_type(self)
        
    def get_q_description(self):
        return Question.get_q_description(self)
        
    def get_topic(self):
        return Question.get_topic(self)
        
    def get_total_marks(self):
        return Question.get_total_marks(self)
        
    def get_exam_id(self):
        return Question.get_exam_id(self)
        
    def get_subques_id(self):
        return self.subques_id 
        
    def get_subques_description(self):
        return self.subques_description 
        
    def get_subques_total_marks(self):
        return self.subques_total_marks 
        
    def get_subques_keywords(self):
        return self.subques_keywords 
        
    def get_subques_answer(self):
        return self.subques_answer 
        
        
class DualEntityQuestion(Question):
    def _init_(self):
        super().__init__(self)
        self.subques_id = None
        self.subques_description = None
        self.subques_total_marks = None
        self.subques_entity1_marks = None
        self.subques_entity2_marks = None
        self.subques_entity1_keywords = None
        self.subques_entity2_keywords = None
        self.subques_entity1_answer = None 
        self.subques_entity2_answer = None
        
    def create_dual_entity_saq(self, q_id, q_desciption, topic, total_marks, exam_id, subques_id, subques_description, subques_total_marks, subques_entity1_marks, subques_entity2_marks, subques_entity1_keywords, subques_entity2_keywords, subques_entity1_answer, subques_entity2_answer):
        Question.create_question(self, q_id, "Dual Entity OEQ", q_desciption, topic, total_marks, exam_id)
        self.subques_id = subques_id
        self.subques_description = subques_description
        self.subques_total_marks = subques_total_marks
        self.subques_entity1_marks = subques_entity1_marks
        self.subques_entity2_marks = subques_entity2_marks
        self.subques_entity1_keywords = subques_entity1_keywords
        self.subques_entity2_keywords = subques_entity2_keywords
        self.subques_entity1_answer = subques_entity1_answer 
        self.subques_entity2_answer = subques_entity2_answer
        
    def set_q_id(self, q_id):
        Question.set_q_id(q_id)
        
    def set_q_type(self):
        Question.set_q_type("Dual Entity OEQ")
        
    def set_q_description(self, q_description):
        Question.set_q_description(q_description)
        
    def set_topic(self, topic):
        Question.set_topic(topic)
        
    def set_total_marks(self, total_marks):
        Question.set_total_marks(total_marks)
        
    def set_exam_id(self, exam_id):
        Question.set_exam_id(exam_id)
        
    def set_subques_id(self, subques_id):
        self.subques_id = subques_id
        
    def set_subques_description(self, subques_description):
        self.subques_description = subques_description
        
    def set_subques_total_marks(self, subques_total_marks):
        self.subques_total_marks = subques_total_marks
        
    def set_subques_entity1_marks(self, subques_entity1_marks):
        self.subques_entity1_marks = subques_entity1_marks
        
    def set_subques_entity2_marks(self, subques_entity2_marks):
        self.subques_entity2_marks = subques_entity2_marks
        
    def set_subques_entity1_keywords(self, subques_entity1_keywords):
        self.subques_entity1_keywords = subques_entity1_keywords
        
    def set_subques_entity2_keywords(self, subques_entity2_keywords):
        self.subques_entity2_keywords = subques_entity2_keywords
        
    def set_subques_entity1_answer(self, subques_entity1_answer):
        self.subques_entity1_answer = subques_entity1_answer
        
    def set_subques_entity2_answer(self, subques_entity2_answer):
        self.subques_entity2_answer = subques_entity2_answer
        
    def get_q_id(self):
        return Question.get_q_id(self)
        
    def get_q_type(self):
        return Question.get_q_type(self)
        
    def get_q_description(self):
        return Question.get_q_description(self)
        
    def get_topic(self):
        return Question.get_topic(self)
        
    def get_total_marks(self):
        return Question.get_total_marks(self)
        
    def get_exam_id(self):
        return Question.get_exam_id(self)
        
    def get_subques_id(self):
        return self.subques_id
        
    def get_subques_description(self):
        return self.subques_description
        
    def get_subques_total_marks(self):
        return self.subques_total_marks
        
    def get_subques_entity1_marks(self):
        return self.subques_entity1_marks
        
    def get_subques_entity2_marks(self):
        return self.subques_entity2_marks
        
    def get_subques_entity1_keywords(self):
        return self.subques_entity1_keywords
        
    def get_subques_entity2_keywords(self):
        return self.subques_entity2_keywords
        
    def get_subques_entity1_answer(self):
        return self.subques_entity1_answer
        
    def get_subques_entity2_answer(self):
        return self.subques_entity2_answer