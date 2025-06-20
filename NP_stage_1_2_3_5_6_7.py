import streamlit as st
from openai import OpenAI
import io
import contextlib

from funcs.get_system_content import get_system_content
from funcs.get_teaching_prompt import get_teaching_prompt
from funcs.get_test_case import get_test_case
from funcs.config_loader import load_config
from funcs.print_chat_history import print_chat_histroy
from funcs.run_test_case import run_test_case
from funcs.handler_user_input import handler_user_input
from funcs.reset_chat import reset_chat
from funcs.get_base_prompt import get_base_prompt

def NP_stage_1_2_3_5_6_7(stage):
    st.title(stage)
    config_name_dict = {
        'NP stage 1. 문제, 명령어 Teaching': ['NP_stage_1', 'gpt-4.1-mini'],
        'NP stage 2. 비교연산자 Teaching': ['NP_stage_2', 'gpt-4.1-mini'],
        'NP stage 3. for문 범위 설정 Teaching': ['NP_stage_3', 'gpt-4.1-mini'],
        'NP stage 5. 대각선 패턴 Teaching': ['NP_stage_5', 'o4-mini'],
        'NP stage 6. 직사각형 패턴 Teaching': ['NP_stage_6', 'o4-mini'],
        'NP stage 7. x, y 연산 패턴 Teaching': ['NP_stage_7', 'o4-mini'],
        'NP stage 8-1. 종합(세로 직선 패턴)': ['NP_stage_8_1', 'o4-mini'],
        'NP stage 8-2. 종합(정사각형 패턴)': ['NP_stage_8_2', 'o4-mini'],
        'NP stage 8-3. 종합((x+y)%5==0 패턴)': ['NP_stage_8_3', 'o4-mini']
    }
    config_name = config_name_dict[stage][0]

    # 사이드바에서 API 키 입력 받기
    st.sidebar.header("API 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)

    gpt_model = config_name_dict[stage][1]
    st.sidebar.markdown('# gpt model')
    st.sidebar.markdown(gpt_model)

    st.sidebar.markdown("# Prompt")
    config = load_config(config_name)
    
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
        if '<명령어 설명>' in prompt:
            back = get_base_prompt(config["first_teaching_base_back"])

        elif '<문제 설명>' in prompt:
            back = get_base_prompt(config["second_teaching_base_back"])

        elif '<범위설정 설명>' in prompt:
            back = get_base_prompt(config["third_teaching_base_back"])

        elif '<제약조건 설명>' in prompt:
            back = get_base_prompt(config["fourth_teaching_base_back"])

        elif '<패턴 설명>' in prompt:
            back = get_base_prompt(config["fifth_teaching_base_back"])

        else :
            back = get_base_prompt(config["sixth_teaching_base_back"])

        prompt_with_base = prompt + back

        handler_user_input(prompt_with_base, client, gpt_model)

    # Test Case 자동실행
    if st.button("▶️ Test Case 실행 (AI는 실수를 할 수 있습니다.)"):
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