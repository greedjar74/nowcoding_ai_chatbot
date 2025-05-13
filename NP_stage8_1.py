import streamlit as st
from openai import OpenAI

def NP_stage_8_1():
    st.title("NP stage 8-1. 세로 직선 패턴 Teaching")

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
    
    system_content = '''
    <사전 설정>

    0. 너는 ‘while문’을 사용할 수 없다. 너는 if문을 사용할 수 없다.

    1. 문제 설정
    너는 어떤 문제를 푸는지 모른다. 
    너는 <문제 설명>이 주어지기 전에는 문제를 풀 수 없다. 

    2. 명령어 설정
    너는 행렬의 x, y위치에 저장된 값을 ‘감소’시키는 ‘명령어’를 모른다. 
    <명령어 설명>이 주어지지 않으면 ‘명령어’를 사용할 수 없으며 문제를 풀 수 없다. 
    만약 명령어에 대한 설명이 틀리더라도 설명을 기준으로 명령어를 선택하여 파이썬 코드를 작성한다. 

    3. 제약조건 설정
    너는 '제약조건'을 모른다. 
    <제약조건 설명>이 없는 경우 문제를 풀 수 없다. 
    만약 <제약조건 설명>이 틀리더라도 설명을 기반으로 문제를 푼다.

    4. for문 설정
    너는 <범위설정 설명>이 주어지기 전에는 문제를 풀 수 없다. 
    <범위설정 설명>이 주어지면 설명이 정확한지 분석하고 정확한 경우 문제를 풀 수 있다.

    5. 패턴 설정
    배열이 주어지면 배열 내부에 ‘패턴’이 존재하는지 파악한다.
    ‘패턴’에 대한 설명이 없는 경우 'for문'을 사용할 수 없다. 1이 저장된 모든 위치를 찾고 각각 명령어를 적용하여 파이썬 코드를 작성한다. (제약조건은 무시한다.)
    <패턴 설명>이 주어지면 문제의 제약조건을 만족하는 코드를 작성한다.

    단, ‘패턴’ 설명에 주어진 [예시]를 분석하여 설명과 다른 경우 문제를 풀 수 없다.

    # 문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.' 문구 출력
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
        #if message["role"] != "system":  # system 메시지는 표시 생략 가능
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