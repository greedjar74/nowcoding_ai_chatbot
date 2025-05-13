import streamlit as st

from NP_stage1 import NP_stage_1
from NP_stage2 import NP_stage_2
from NP_stage3 import NP_stage_3
from NP_stage4 import NP_stage_4
from NP_stage5 import NP_stage_5
from NP_stage6 import NP_stage_6
from NP_stage7 import NP_stage_7
from NP_stage8_1 import NP_stage_8_1
from NP_stage8_2 import NP_stage_8_2
from NP_stage8_3 import NP_stage_8_3

def NP_main():
    stages = ['NP stage1. 문제, 명령어 Teaching', 
              'NP stage2. 제약조건 Teaching', 
              'NP stage3. 비교연산자 Teaching', 
              'NP stage4. for문 범위 설정 Teaching',
              'NP stage5. 대각선 패턴 Teaching', 
              'NP stage6. 직사각형 패턴 Teaching', 
              'NP stage7. x, y 연산 패턴 Teaching', 
              'NP stage8-1. 종합(세로 직선 패턴)',
              'NP stage8-2. 종합(정사각형 패턴)', 
              'NP stage8-3. 종합((x+y)%5==0 패턴)']
    
    selected_stage = st.sidebar.selectbox('stage를 선택하세요.', stages)

    # 이전 페이지와 다르면 메시지 초기화
    if "previous_stage" not in st.session_state:
        st.session_state.previous_stage = selected_stage
    elif st.session_state.previous_stage != selected_stage:
        st.session_state.pop("messages", None)  # 메시지 초기화
        st.session_state.previous_stage = selected_stage

    if selected_stage == 'NP stage1. 문제, 명령어 Teaching':
        NP_stage_1()
    elif selected_stage == 'NP stage2. 제약조건 Teaching':
        NP_stage_2()
    elif selected_stage == 'NP stage3. 비교연산자 Teaching':
        NP_stage_3()
    elif selected_stage == 'NP stage4. for문 범위 설정 Teaching':
        NP_stage_4()
    elif selected_stage == 'NP stage5. 대각선 패턴 Teaching':
        NP_stage_5()
    elif selected_stage == 'NP stage6. 직사각형 패턴 Teaching':
        NP_stage_6()
    elif selected_stage == 'NP stage7. x,y 연산 패턴 Teaching':
        NP_stage_7()
    elif selected_stage == 'NP stage8-1. 종합(세로 직선 패턴)':
        NP_stage_8_1()
    elif selected_stage == 'NP stage8-2. 종합(정사각형 패턴)':
        NP_stage_8_2()
    else :
        NP_stage_8_3()