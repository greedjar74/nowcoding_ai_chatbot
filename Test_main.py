import streamlit as st

from test_page import test_page

def Test_main():
    stages = [
        'Test page'
    ]

    # 현재 선택된 페이지
    selected_stage = st.sidebar.selectbox('stage를 선택하세요.', stages)

    # 이전 페이지와 다르면 메시지 초기화
    if "previous_stage" not in st.session_state:
        st.session_state.previous_stage = selected_stage
    elif st.session_state.previous_stage != selected_stage:
        st.session_state.pop("messages", None)  # 메시지 초기화
        st.session_state.previous_stage = selected_stage

    # 각 페이지 연결
    if selected_stage == 'Test page':
        test_page()