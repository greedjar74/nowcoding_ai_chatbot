import streamlit as st

from MZ_stage_3_for import MZ_stage_3_for
from MZ_stage_3_command import MZ_stage_3_command
from MZ_stage_4_nestedloop import MZ_stage_4_nestedloop
from MZ_stage_4_while_notDone import MZ_stage_4_while_notDone
from MZ_stage_5 import MZ_stage_5
from MZ_stage_6 import MZ_stage_6
from MZ_stage_7 import MZ_stage_7

def MZ_main():
    stages = [
        'MZ stage3. 명령어 Teaching',
        'MZ stage3. for문 Teaching',
        'MZ stage4. 중첩반복문 Teaching',
        'MZ stage4. while, NotDone() Teaching',
        'MZ stage5. if문, 조건 명령어 Teaching',
        'MZ stage6. else문 Teaching',
        'MZ stage7. elif문, 갈림길 명령어 Teaching'
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
    if selected_stage == 'MZ stage3. 명령어 Teaching':
        MZ_stage_3_command()
    elif selected_stage == 'MZ stage3. for문 Teaching':
        MZ_stage_3_for()
    elif selected_stage == 'MZ stage4. 중첩반복문 Teaching':
        MZ_stage_4_nestedloop()
    elif selected_stage == 'MZ stage4. while, NotDone() Teaching':
        MZ_stage_4_while_notDone()
    elif selected_stage == 'MZ stage5. if문, 조건 명령어 Teaching':
        MZ_stage_5()
    elif selected_stage == 'MZ stage6. else문 Teaching':
        MZ_stage_6()
    else:
        MZ_stage_7()
