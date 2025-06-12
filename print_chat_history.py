import streamlit as st

def print_chat_histroy(messages):
    # 이전 메시지 출력
    for message in messages:
        if message["role"] != "system":  # system 메시지는 표시 생략 가능
            with st.chat_message(message["role"]):
                # gpt가 생성한 답변은 python 형태로 출력
                if message['role'] == 'assistant':
                    st.code(message['content'], language='python')
                else :
                    st.text(message["content"])