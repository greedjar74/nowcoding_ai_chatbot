import streamlit as st

from MZ_stage_page import MZ_stage_page

def MZ_main():
    stages = [
        'MZ stage 3. 명령어 Teaching',
        'MZ stage 3. for문 Teaching',
        'MZ stage 4. 중첩반복문 Teaching',
        'MZ stage 4. while, NotDone() Teaching',
        'MZ stage 5. if문, 조건 명령어 Teaching',
        'MZ stage 6. else문 Teaching',
        'MZ stage 7. elif문, 갈림길 명령어 Teaching'
    ]

    # 현재 선택된 페이지
    selected_stage = st.sidebar.selectbox('stage를 선택하세요.', stages)

    # 이전 페이지와 다르면 메시지 초기화
    if "previous_stage" not in st.session_state:
        st.session_state.previous_stage = selected_stage
    elif st.session_state.previous_stage != selected_stage:
        st.session_state.pop("messages", None)  # 메시지 초기화
        st.session_state.previous_stage = selected_stage

    MZ_stage_page(selected_stage)