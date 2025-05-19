import streamlit as st
from PIL import Image

from MZ_main import MZ_main
from NP_main import NP_main
from test import test

def main_page():
    st.title('나우코딩랩스 생성형 AI 실습')
    st.write('각 stage에 대한 실습을 진행하세요.')

    st.markdown("## API key 입력")
    api_img = Image.open("api_key_input.PNG")
    st.image(api_img)
    st.text("- API key를 box에 입력해주세요.")

    st.markdown("## gpt model")
    model_img = Image.open("gpt_model.PNG")
    st.image(model_img)
    st.text("- 해당 stage에서 사용하는 gpt model")

    st.markdown("## System Content")
    sc_img = Image.open("system_content.PNG")
    st.image(sc_img)
    st.text('''
            - system content prompt
            - 입력하지 마세요.
            ''')
    
    st.markdown("## Teaching Prompt")
    tp_img = Image.open("teaching_prompt.PNG")
    st.image(tp_img)
    st.text('''
            - AI Teaching을 위한 prompt
            - 설명을 개별적으로 입력해주세요.
            ''')
    
    st.markdown("## Test Case")
    tc_img = Image.open("test_case.PNG")
    st.image(tc_img)
    st.text('''
            - Teaching의 정확도를 확인하기 위한 Test Case
            - 각 문제를 개별적으로 입력해주세요
            ''')


page_names_to_funcs = {'Main Page': main_page, 'MZ 실습': MZ_main, 'NP 실습': NP_main, 'Test': test}

selected_page = st.sidebar.selectbox('Select a stage', page_names_to_funcs.keys())

page_names_to_funcs[selected_page]()