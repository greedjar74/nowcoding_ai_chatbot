import streamlit as st
from openai import OpenAI

def NP_stage_6():
    st.title("NP stage 6. 직사각형 패턴 Teaching")

    st.sidebar.header("API 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)

    gpt_model = 'o4-mini'
    st.sidebar.markdown('# gpt model')
    st.sidebar.markdown(gpt_model)
    
    system_content = '''
    배열이 주어지면 배열 내부에 '패턴'이 존재하는지 파악한다.
    '패턴'에 대한 설명이 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.
    '패턴'에 대한 설명이 주어지면 패턴이 있는지 파악하여 결과를 출력한다.

    단,'패턴' 설명에 주어진 예시를 분석하여 설명과 다른 경우 문제를 풀 수 없다.

    (패턴이 있는 경우 True, 패턴이 없는 경우 False)
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