import streamlit as st
from openai import OpenAI
import numpy as np

st.title("NP stage3. 비교연산자 Teaching")

client = OpenAI(api_key="")  # 여기에 API 키 입력 또는 secrets 사용
system_content = '''
너는 <비교연산자 설명>이 주어지기 전에는 문제를 풀 수 없다.
<비교연산자 설명>이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 '비교연산자(<, >, ==, !=, <=, >=)'를 사용할 수 있다.
설명이 없는 '비교연산자'는 사용할 수 없다.

문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.'를 출력한다.

<기본 명령어>
erase(x, y): x행, y열에 저장된 값을 1 감소시킨다.
(따로 정의할 필요 없다.)        
'''

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1-mini"  # 모델명은 정확히 확인 필요

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
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
