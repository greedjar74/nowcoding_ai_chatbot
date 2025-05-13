import streamlit as st
from openai import OpenAI

def NP_stage_3():
    st.title("NP stage3. 비교연산자 Teaching")

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
    
    system_content = '''
    너는 <비교연산자 설명>이 주어지기 전에는 문제를 풀 수 없다.
    <비교연산자 설명>이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 '비교연산자(<, >, ==, !=, <=, >=)'를 사용할 수 있다.
    설명이 없는 '비교연산자'는 사용할 수 없다.

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.'를 출력한다.

    <기본 명령어>
    erase(x, y): x행, y열에 저장된 값을 1 감소시킨다.
    (따로 정의할 필요 없다.)        
    '''

    st.sidebar.markdown('# system content')
    st.sidebar.markdown(system_content)

    # ✅ system message를 포함한 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":  # system 메시지는 표시 생략 가능
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
