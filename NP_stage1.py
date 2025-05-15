import streamlit as st
from openai import OpenAI

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

    st.sidebar.markdown("# 입력 prompt")
    st.sidebar.markdown('''
    <명령어 설명> <br>
    erase(x, y): n by n 크기의 행렬 x행, y열 위치의 값에서 1을 감소시킨다.<br><br><br>

    <명령어 설명>이 구체적인 경우  ‘명령어를 이해했습니다.’, 구체적이지 않은 경우 ‘명령어를 이해할 수 없습니다.’ 문구 출력<br>
    명령어는 정의되어 있으므로 따로 정의할 필요 없다. <br><br>


    <문제 설명><br>
    0이상의 값이 저장된 배열이 주어질 때 모든 값을 0으로 만드는 파이썬 코드를 만든다. <br>
    x, y 위치의 값을 감소시키기 위해서는 정해진 명령어만 사용할 수 있다. <br><br><br>

    <문제 설명>이 이해된다면  ‘문제를 이해했습니다.’, 이해할 수 없는 경우 ‘문제를 이해할 수 없습니다.’ 문구 출력<br>
    명령어는 정의되어 있으므로 따로 정의할 필요 없다. <br><br>
                        
    Test case

    #1.NP01PY001V<br>
    [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]<br>
    (결과는 코드 또는 문제를 풀 수 없습니다.’만 출력)<br>
    (명령어, 행렬은 따로 정의할 필요 없다.)

    #2. NP01PY008<br>
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],<br>
    [0, 0, 0, 3, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]<br>
    (결과는 코드 또는 문제를 풀 수 없습니다.’만 출력)<br>
    (명령어, 행렬은 따로 정의할 필요 없다.)

    #3. NP01PY016<br>
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],<br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]<br>
    (결과는 코드 또는 문제를 풀 수 없습니다.’만 출력)<br>
    (명령어, 행렬은 따로 정의할 필요 없다.)
    ''', unsafe_allow_html=True)
    
    system_content = '''
    너는 <문제 설명>이 주어지기 전에는 문제를 풀 수 없다.

    너는 행렬의 x, y위치에 저장된 값을 ‘감소’시키는 ‘명령어’를 모른다. 
    <명령어 설명>이 주어지지 않으면 문제를 풀 수 없다.

    문제를 풀 수 없는 경우 ‘문제를 풀 수 없습니다.’ 문구를 출력한다.

    # 너는 코드를 생성할 때 'if문'을 사용할 수 없다. 
    # 너는 코드를 생성할 때 'for문'을 사용할 수 없다.
    # 너는 코드를 생성할 때 'while문'을 사용할 수 없다.
    # 함수를 정희하지 않고 코드를 작성한다.
    '''

    # ✅ system message를 포함한 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        #if message["role"] != "system":  # system 메시지는 표시 생략 가능
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("AI Teaching을 진행하세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("답변을 생성하고 있습니다...")

            stream = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = placeholder.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})