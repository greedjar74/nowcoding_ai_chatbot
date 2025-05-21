import streamlit as st
from openai import OpenAI

def test_page():
    st.title("Test")

    st.sidebar.markdown("# Test page")
    st.sidebar.text("자유롭게 테스트하세요.")
    st.sidebar.text("(대화 기록이 남아있는 경우 다른 stage로 한 번 이동해주세요.)")

    # 사이드바에서 gpt model 입력 받기
    st.sidebar.markdown("# gpt model 설정")
    models = ['gpt-4o-mini',
              'gpt-4.1-mini',
              'o4-mini',
              '직접 입력']
    selected_model = st.sidebar.selectbox('model을 선택하세요.', models)
    
    if selected_model == '직접 입력':
        gpt_model = st.sidebar.text_input('gpt model을 입력하세요.')
        if not gpt_model:
            st.warning("gpt model을 사이드바에 입력해주세요.")
            return
    else :
        gpt_model = selected_model
    
    # 사이드바에서 API 키 입력 받기
    st.sidebar.markdown("# API key 설정")
    api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if not api_key_input:
        st.warning("API 키를 사이드바에 입력해주세요.")
        return

    client = OpenAI(api_key=api_key_input)
    
    # 사이드바에서 system content 입력 받기
    st.sidebar.markdown("# System content 입력")
    system_content = st.sidebar.text_area("System content")

    if not system_content:
        st.warning("System content를 사이드바에 입력해주세요.")
        return

    # ✅ system message를 포함한 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_content}
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        #if message["role"] != "system":  # system 메시지는 표시 생략 가능
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