import streamlit as st
from openai import OpenAI
import io
import contextlib

from get_system_content import get_system_content
from get_teaching_prompt import get_teaching_prompt
from get_test_case import get_test_case
from config_loader import load_config
from print_chat_history import print_chat_histroy
from funcs.run_test_case import run_test_case
from handler_user_input import handler_user_input
from funcs.reset_chat import reset_chat

def NP_stage_1():
    st.title("NP stage 1. 문제, 명령어 Teaching")

    # 사이드바에서 API 키 입력 받기
    st.sidebar.header("API 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)

    gpt_model = 'gpt-4.1-mini'
    st.sidebar.markdown('# gpt model')
    st.sidebar.markdown(gpt_model)

    st.sidebar.markdown("# Prompt")
    config = load_config("NP_stage_1")
    
    # system content 불러오기
    system_content = get_system_content(config['system_content_path'])

    # system content 보기 옵션
    show_system_content = st.sidebar.checkbox("System Content 보기", value=False)
    if show_system_content:    
        st.sidebar.markdown("### System Content")
        st.sidebar.text(system_content)

    # teaching prompt 불러오기
    teaching_prompt = get_teaching_prompt(config['teaching_prompt_path'])

    # teaching prompt 보기 옵션
    show_teaching_prompt = st.sidebar.checkbox("Teaching Prompt 보기", value=False)
    if show_teaching_prompt:   
        st.sidebar.markdown("### Teaching Prompt")
        st.sidebar.text(teaching_prompt)
    
    # Test case
    test_case = get_test_case(config['test_case_path'])
    st.sidebar.markdown("# Test Case")
    st.sidebar.text(config['test_case_label'])
    st.sidebar.image(config['test_case_image'])

    # ✅ system message를 포함한 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]

    # 이전 메시지 출력
    print_chat_histroy(st.session_state.messages)

    # 사용자 입력 처리
    if prompt := st.chat_input("AI Teaching을 진행하세요!"):
        handler_user_input(prompt, client, gpt_model)

    # Test Case 자동실행
    if st.button("▶️ Test Case 실행"):
        print(test_case)
        run_test_case(test_case, client, gpt_model)

    # 🔁 대화 리셋 버튼 (system 메시지 제외)
    if st.button("⚠️ 대화 리셋"):
        reset_chat()

    with open(config['default_code_path'], 'r', encoding='utf-8') as f:
        default_code = f.read()


    # 텍스트 영역에 기본값으로 코드 표시
    input_code = st.text_area("gpt가 생성한 코드를 입력하세요", value="", height=100)

    with open(config['run_code_path'], 'r', encoding='utf-8') as f:
        run_code = f.read()

    code = default_code + '\n' + input_code + '\n' + run_code
    if st.button("코드 실행"):
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code, {})
            st.success("실행 성공!")
        except Exception as e:
            st.error(f"오류 발생: {e}")
        st.text("출력 결과:")

        with open(config['result_base_path'], 'r', encoding='utf-8') as f:
            result_base = f.read()
            
        st.code(result_base + output.getvalue())