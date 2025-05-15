import streamlit as st
from openai import OpenAI

def MZ_stage_6():
    st.title("MZ stage 6. else문 Teaching")

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
    너는 <else문 설명>'이 주어지기 전에는 문제를 풀 수 없다.
    'else문'에 대한 설명이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 문제를 풀 수 있다.
    설명에 '예시'가 없는 경우 문제를 풀 수 없다.

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.

    <기본 명령어 설명> 
    moveForward(): 아바타를 한 칸 앞으로 이동시킨다. 
    turnLeft(): 아바타를 왼쪽으로 90도 회전시킨다. 
    turnRight(): 아바타를 오른쪽으로 90도 회전시킨다.
    pathAhead(): 아바타 앞에 길이 있는지 확인한다. 길이 있는 경우 True
    pathLeft(): 아바타 왼쪽에 길이 있는지 확인한다. 길이 있는 경우 True
    pathRight(): 아바타 오른쪽에 길이 있는지 확인한다. 길이 있는 경우 True
    notDone(): 아바타가 도착지에 도착했는지 파악한다. 도착하지 못한 경우 True
    '''

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
