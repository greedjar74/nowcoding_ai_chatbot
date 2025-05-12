import streamlit as st
from openai import OpenAI

def NP_stage_1():
    st.title("NP stage1. 문제, 명령어 Teaching")

    client = OpenAI(api_key=st.secrets['api']['key'])
    
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
