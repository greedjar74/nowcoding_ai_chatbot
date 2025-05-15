import streamlit as st
from openai import OpenAI

def NP_stage_4():
    st.title("NP stage 4. for문 범위 설정 Teaching")

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
    <범위설정 설명> <br>
    range(start, end, term) : ‘start’부터 ‘end-1’까지 ‘term’ 간격으로 증가한다.<br>

    [예시]<br>
    for i in range(start, end, term):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;동작코드<br><br><br>


    <범위설정 설명>이 정확한 경우 '범위설정 설명을 이해했습니다.', 정확하지 않은 경우 '범위설정 설명을 이해하지 못했습니다.' 문구를 출력한다. <br>
    ([예시]가 없거나 정확하지 않은 경우 이해할 수 없다.) <br>
    (설명에서 range에 입력한 'end'보다 1 작은 값까지 수행된다는 설명이 정확히 표현되었는지 확인한다.)<br><br>
                        
    Test case <br>
    각 문제에 맞는 코드를 작성한다. 결과는 코드 또는 ‘제가 모르는 부분입니다.’만 출력한다.

    #1. NP04PY001V<br>
    i가 0부터 4까지 1씩 진행되는 동안 erase(5, 3)을 수행한다. i가 3부터 7까지 1씩 증가하는 동안 erase(i, 6)을 수행한다.<br>
    (<범위설정 설명>에서 '범위설정 설명을 이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (erase 명령어는 따로 정의하지 않아도 된다.)

    #2. NP04PY007<br>
    i가 2부터 8까지 2씩 증가하는 동안 erase(i, 4)를 수행한다. j가 4부터 7까지 3씩 증가하는 동안 erase(4, j)를 수행한다.<br>
    (<범위설정 설명>에서 '범위설정 설명을 이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>                    
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (erase 명령어는 따로 정의하지 않아도 된다.)

    #3. NP04PY016<br>
    i가 1부터 9까지 2씩 증가하는 동안 erase(i, 5), erase(6, i)를 수행한다.<br>
    (<범위설정 설명>에서 '범위설정 설명을 이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (erase 명령어는 따로 정의하지 않아도 된다.)

    #4. NP04PY011<br>
    i가 1부터 9까지 1씩 증가하는 동안 erase(i, i)를 수행한다. i가 1부터 7까지 2씩 증가하는 동안 erase(i, 5)를 수행한다.<br>.
    (<범위설정 설명>에서 '범위설정 설명을 이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (erase 명령어는 따로 정의하지 않아도 된다.)
    ''', unsafe_allow_html=True)
    
    system_content = '''
    너는 ‘while문’을 사용할 수 없다. 

    너는 <범위설정 설명>이 주어지기 전에는 문제를 풀 수 없다.
    <범위설정 설명>이 주어지면 설명이 정확한지 분석하고 정확한 경우 문제를 풀 수 있다.

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.
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