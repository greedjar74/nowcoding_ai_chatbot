import streamlit as st
from MZ_main import MZ_main
from NP_main import NP_main

def main_page():
    st.title('나우코딩랩스 생성형 AI 실습')
    st.write('각 stage에 대한 실습을 진행하세요.')

page_names_to_funcs = {'Main Page': main_page, 'MZ': MZ_main, 'NP': NP_main}

selected_page = st.sidebar.selectbox('Select a stage', page_names_to_funcs.keys())

page_names_to_funcs[selected_page]()