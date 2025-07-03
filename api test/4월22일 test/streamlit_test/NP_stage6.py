import streamlit as st
from openai import OpenAI
import numpy as npㅈ


st.title("NP stage6. 직사각형 패턴 Teaching")

client = OpenAI(api_key="")  # 여기에 API 키 입력 또는 secrets 사용
system_content = '''
배열이 주어지면 배열 내부에 '패턴'이 존재하는지 파악한다.
'패턴'에 대한 설명이 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.
'패턴'에 대한 설명이 주어지면 패턴이 있는지 파악하여 결과를 출력한다.

단,'패턴' 설명에 주어진 예시를 분석하여 설명과 다른 경우 문제를 풀 수 없다.

(패턴이 있는 경우 True, 패턴이 없는 경우 False)
'''

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "o4-mini"  # 모델명은 정확히 확인 필요

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
