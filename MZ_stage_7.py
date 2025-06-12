import streamlit as st
from openai import OpenAI

def MZ_stage_7():
    st.title("MZ stage 7. elif문 & 갈림길 명령어 Teaching")

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

    # system content
    with open('system_contents/MZ_stage_7.txt', 'r', encoding='utf-8') as f:
        system_content = f.read()    
    st.sidebar.markdown("# System Content")
    st.sidebar.text(system_content)

    # teaching prompt
    with open('input_contents/MZ_stage_7.txt', 'r', encoding='utf-8') as f:
        teaching_prompt = f.read()    
    st.sidebar.markdown("# Teaching Prompt")
    st.sidebar.text(teaching_prompt)
    
    # Test case
    with open('test_cases/MZ_stage_7.txt', 'r', encoding='utf-8') as f:
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
                # gpt가 생성한 답변은 python 형태로 출력
                if message['role'] == 'assistant':
                    st.code(message['content'], language='python')
                else :
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

            placeholder.code(response, language='python') # gpt가 생성한 답변은 python 형태로 출력
 
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Test Case 자동실행
    if st.button("▶️ Test Case 실행"):
        print(test_case)
        st.session_state.messages.append({"role": "user", "content": test_case})
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

            placeholder.code(response, language='python')

        st.session_state.messages.append({"role": "assistant", "content": response})

    # 🔁 대화 리셋 버튼 (system 메시지 제외)
    if st.button("⚠️ 대화 리셋"):
        system_message = next((m for m in st.session_state.messages if m["role"] == "system"), None)
        st.session_state.messages = []
        if system_message:
            st.session_state.messages.append(system_message)
        st.rerun()