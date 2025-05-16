import streamlit as st
from openai import OpenAI

def NP_stage_8_2():
    st.title("NP stage 8-2. 정사각형 패턴 Teaching")

    # 사이드바에서 API 키 입력 받기
    st.sidebar.header("API 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)

    gpt_model = 'o4-mini'
    st.sidebar.markdown('# gpt model')
    st.sidebar.markdown(gpt_model)
    
    # system content 설정
    with open(r'system_contents\NP_stage_8_2.txt', 'r', encoding='utf-8') as f:
        system_content = f.read()
    
    st.sidebar.markdown("# System Content")
    st.sidebar.text(system_content)

    # 설명 prompt
    with open(r'input_contents\NP_stage_8_2.txt', 'r', encoding='utf-8') as f:
        input_prompt = f.read()
    
    st.sidebar.markdown("# 설명 Prompt")
    st.sidebar.text(input_prompt)

    # Test Case
    with open(r'test_cases\NP_stage_8_2.txt', 'r', encoding='utf-8') as f:
        test_case = f.read()

    st.sidebar.markdown("# Test Case")
    st.sidebar.text(test_case)

    # ✅ system message를 포함한 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":  # system 메시지는 표시 생략 가능
            with st.chat_message(message["role"]):
                st.text(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("AI Teaching을 진행하세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.text(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.text("답변을 생성하고 있습니다...")

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