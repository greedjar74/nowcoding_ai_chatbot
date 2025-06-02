import streamlit as st
from openai import OpenAI
import io
import contextlib

def NP_stage_3():
    st.title("NP stage 3. for문 범위 설정 Teaching")

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
    
    # system content
    with open('system_contents/NP_stage_3.txt', 'r', encoding='utf-8') as f:
        system_content = f.read()    
    st.sidebar.markdown("# System Content")
    st.sidebar.text(system_content)

    # teaching prompt
    with open('input_contents/NP_stage_3.txt', 'r', encoding='utf-8') as f:
        teaching_prompt = f.read()    
    st.sidebar.markdown("# Teaching Prompt")
    st.sidebar.text(teaching_prompt)
    
    # Test case
    with open('test_cases/NP_stage_3.txt', 'r', encoding='utf-8') as f:
        test_case = f.read()    
    st.sidebar.markdown("# Test Case")
    st.sidebar.text(test_case)
    
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

    # 기본 코드 설정
    default_code = '''# 예시 코드
def erase(x, y):
    board[x][y] -= 1
        
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 5, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    '''

    # 텍스트 영역에 기본값으로 코드 표시
    input_code = st.text_area("여기에 파이썬 코드를 입력하세요", value="", height=200)

    run_code = ''' # 실행 코드
for l in board:
    print(l)
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 5, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#after
''' 
        st.code(result + output.getvalue())