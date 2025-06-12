import streamlit as st
from openai import OpenAI
import io
import contextlib

from get_system_content import get_system_content
from get_teaching_prompt import get_teaching_prompt
from get_test_case import get_test_case
from config_loader import load_config

def NP_stage_8_3():
    st.title("NP stage 8-3. (x+y)%5==0 패턴 Teaching")

    # 사이드바에서 API 키 입력 받기
    st.sidebar.header("API 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)

    gpt_model = 'o4-mini'
    st.sidebar.markdown('# gpt model')
    st.sidebar.markdown(gpt_model)
    
    st.sidebar.markdown("# Prompt")
    config = load_config("NP_stage_8_3")
    
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
    for message in st.session_state.messages:
        if message["role"] != "system":  # system 메시지는 표시 생략 가능
            with st.chat_message(message["role"]):
                # gpt가 생성한 답변은 python 형태로 출력
                if message['role'] == 'assistant':
                    st.code(message['content'], language='python')
                else :
                    st.text(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("AI Teaching을 진행하세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.text(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.text("답변을 생성하고 있습니다...")

            stream = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = placeholder.write_stream(stream)

            placeholder.code(response, language='python') # gpt가 생성한 답변은 python 형태로 출력

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Test Case 자동실행
    if st.button("▶️ Test Case 실행"):
        print(test_case)
        st.session_state.messages.append({"role": "user", "content": test_case})
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.text("답변을 생성하고 있습니다...")

            stream = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = placeholder.write_stream(stream)

            placeholder.code(response, language='python')

        st.session_state.messages.append({"role": "assistant", "content": response})

    # 🔁 대화 리셋 버튼 (system 메시지 제외)
    if st.button("⚠️ 대화 리셋"):
        system_message = next((m for m in st.session_state.messages if m["role"] == "system"), None)
        st.session_state.messages = []
        if system_message:
            st.session_state.messages.append(system_message)
        st.rerun()

    # 기본 코드 설정
    default_code = '''# 예시 코드
def erase(x, y):
    board[x][y] -= 1
        
board = [[1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
[0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
[0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
[0, 0, 0, 1, 0, 0, 0, 0, 1, 0], 
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0], 
[0, 1, 0, 0, 0, 0, 1, 0, 0, 0]]
    '''

    # 텍스트 영역에 기본값으로 코드 표시
    input_code = st.text_area("gpt가 생성한 코드를 입력하세요", value="", height=100)

    run_code = ''' # 실행 코드
for l in board:
    print(l)

re = True
for i in range(10):
    for j in range(10):
        if board[i][j] != 0:
            re = False
            break
    if not re:
        break
        
print()
if re:
    print("모든 폭탄을 제거했습니다.")
else :
    print("폭탄을 제거하지 못헸습니다.")
    '''

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
        result = '''
# before
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
[0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
[0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
[0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0] 
[0, 0, 0, 0, 1, 0, 0, 0, 0, 1] 
[0, 0, 0, 1, 0, 0, 0, 0, 1, 0] 
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0] 
[0, 1, 0, 0, 0, 0, 1, 0, 0, 0]

#after
''' 
        st.code(result + output.getvalue())