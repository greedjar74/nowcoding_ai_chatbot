import streamlit as st
from openai import OpenAI

def NP_stage_2():
    st.title("NP stage 2. 제약조건 Teaching")

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
    
    st.sidebar.markdown("# 입력 prompt")
    st.sidebar.markdown('''
    <제약조건 설명> <br>
    for문을 코드에 한 번 명시할 때마다 반복문 사용 횟수를 1 증가시킨다. <br>
    erase 명령어를 코드에 한 번 명시할 때마다 커맨드 사용 횟수를 1 증가시킨다. <br>
    단, 반복문에 의한 중복 호출은 무시한다. <br><br><br>

    설명이 구체적인 경우 ‘제약조건을 이해했습니다.’, 구체적으로 작성되지 않은 경우 ‘제약조건을 이해할 수 없습니다.’ 문구를 출력한다. <br>
    (‘제약조건을 이해할 수 없습니다.’ 출력시 문제를 풀 수 없다.)<br><br>
                        
    Test case <br>
    각각의 문제에 대한 결과를 출력한다. <br>
    (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)

    [출력 형식] <br>
    반복문 : n개 <br>
    커맨드 : m개

    #1. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    erase(0, 0)

    #2. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    erase(0, 0)<br>
    erase(0, 1)<br>
    erase(0, 2)<br>
    erase(0, 3)

    #3. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    erase(0, 0)<br>
    erase(0, 0)<br>
    erase(0, 0)<br>
    erase(0, 0)


    #4. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    for i in range(10):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(0, i)

    #5. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    for i in range(5):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(0, i)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(i, 0)

    #6. (<제약조건 설명>에서 '제약조건을 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    for i in range(5):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(0, i)

    for i in range(5):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(0, i)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;erase(0, 0)


    ''', unsafe_allow_html=True)

    system_content = '''
    너는 '제약조건'을 모른다. 
    <제약조건 설명>이 없는 경우 문제를 풀 수 없다. 
    만약 <제약조건 설명>이 틀리더라도 설명을 기반으로 문제를 푼다. 

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.
    '''

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