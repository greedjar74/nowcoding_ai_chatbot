import streamlit as st
from openai import OpenAI

def NP_stage_3():
    st.title("NP stage 3. 비교연산자 Teaching")

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
    <비교연산자 설명> <br>
    a < b : a가 b보다 작은지 확인한다. a가 작은 경우 True <br>
    a == b : 두 값이 동일한지 확인한다. 동일한 경우 True <br>
    a != b : 두 값이 다른지 확인한다. 다른 경우 True <br>
    a <= b : a가 b보다 작거나 같은지 확인한다. a가 작거나 같은 경우 True <br><br><br>

    <비교연산자 설명>이 정확한지 분석한다. 정확한 경우 '비교연산자를 이해했습니다.' 정확하지 않은 경우 '비교연산자를 이해하지 못했습니다.' 문구를 출력한다. <br>
    ('비교연산자를 이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.)<br><br>
                        
    Test case <br>
    각 문제에 맞는 코드를 작성한다. 결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력한다.

    #1. NP03PY001V<br>
    i는 2를 초기값으로 가진다. i가 9보다 작은 경우 erase(i, 3)과 i+=2를 반복한다.<br>
    (결과는 코드 또는 ‘’문제를 풀 수 없습니다.’만 출력)<br>
    (명령어는 정의할 필요 없다.)

    #2. NP03PY019<br>
    x의 초기값은 1, y의 초기값은 2다. x가 10보다 작거나 같은 경우 erase(x, y)와 x+=3, y+=2를 반복한다.<br>
    (결과는 코드 또는 ‘’문제를 풀 수 없습니다.’만 출력)<br>
    (명령어는 정의할 필요 없다.)

    #3. NP03PY021<br>
    x의 초기값은 2, y1의 초기값은 2, y2의 초기값은 9이다. x가 9보다 작거나 같은 경우 erase(x, y1), erase(x, y2), x += 7을 반복한다.<br>
    (결과는 코드 또는 ‘’문제를 풀 수 없습니다.’만 출력)<br>
    (명령어는 정의할 필요 없다.)

    #4. NP03PY020<br>
    x1=2, y1=8, x2=6, y2=6을 초기값으로 가진다. x1이 5보다 작거나 같은 경우 erase(x1, y1), x1 += 1, y1-=1을 반복한다. x2가 9보다 작거나 같은 경우 erase(x2, y2), x2+=1, y2+=1을 반복한다.<br>
    (결과는 코드 또는 ‘’문제를 풀 수 없습니다.’만 출력)<br>
    (명령어는 정의할 필요 없다.)
    ''', unsafe_allow_html=True)
    
    system_content = '''
    너는 <비교연산자 설명>이 주어지기 전에는 문제를 풀 수 없다.
    <비교연산자 설명>이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 '비교연산자(<, >, ==, !=, <=, >=)'를 사용할 수 있다.
    설명이 없는 '비교연산자'는 사용할 수 없다.

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.'를 출력한다.

    <기본 명령어>
    erase(x, y): x행, y열에 저장된 값을 1 감소시킨다.
    (따로 정의할 필요 없다.)        
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