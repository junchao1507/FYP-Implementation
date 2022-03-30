# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 20:59:27 2022

@author: Lenovo
"""

# Importing packages
import streamlit as st
from hydralit import HydraHeadApp
from PIL import Image

class NewSingleEntitySAQPage(HydraHeadApp):    
    def run(self):
        st.write('---')