import streamlit as st
from openai import OpenAI

def MZ_stage_3_for():
    st.title("MZ stage3. for문 Teaching")

    client = OpenAI(api_key=st.secrets['api']['key'])

    system_content = '''
    너는 파이썬의 'while문'을 사용할 수 없다. 

    너는 <for문 설명>이 주어지기 전에는 사용할 수 없다. 
    'for문 설명'이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 'for문'을 사용할 수 있다.
    예시가 없다면 'for문'을 사용할 수 없다.
    문제가 주어졌을 때 'for문'을 사용하지 못하는 상황에서는 'for문' 없이 코드를 작성한다.

    <기본 명령어 설명>
    moveForward(): 아바타를 한 칸 앞으로 이동시킨다.
    turnLeft(): 아바타를 왼쪽으로 90도 회전시킨다.
    turnRight(): 아바타를 오른쪽으로 90도 회전시킨다.
    '''

    gpt_model = 'gpt-4.1-mini'

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
