import streamlit as st

from NP_stage4 import NP_stage_4
from NP_stage_1_2_3_5_6_7 import NP_stage_1_2_3_5_6_7

def NP_main():
    stages = ['NP stage 1. 문제, 명령어 Teaching',
              'NP stage 2. 비교연산자 Teaching', 
              'NP stage 3. for문 범위 설정 Teaching', 
              'NP stage 4. 제약조건 Teaching', 
              'NP stage 5. 대각선 패턴 Teaching', 
              'NP stage 6. 직사각형 패턴 Teaching', 
              'NP stage 7. x, y 연산 패턴 Teaching', 
              'NP stage 8-1. 종합(세로 직선 패턴)',
              'NP stage 8-2. 종합(정사각형 패턴)', 
              'NP stage 8-3. 종합((x+y)%5==0 패턴)']
    
    selected_stage = st.sidebar.selectbox('stage를 선택하세요.', stages)

    # 이전 페이지와 다르면 메시지 초기화
    if "previous_stage" not in st.session_state:
        st.session_state.previous_stage = selected_stage
    elif st.session_state.previous_stage != selected_stage:
        st.session_state.pop("messages", None)  # 메시지 초기화
        st.session_state.previous_stage = selected_stage

    if selected_stage == 'NP stage 4. 제약조건 Teaching':
        NP_stage_4()
    else:
        NP_stage_1_2_3_5_6_7(selected_stage)