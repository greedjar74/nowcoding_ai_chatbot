import streamlit as st
from openai import OpenAI

def MZ_stage_4_nestedloop():
    st.title("MZ stage 4. 중첩반복문 Teaching")

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
    <중첩 반복문 설명> <br>
    중첩 반복문: for문 내부에 또 다른 for문이 포함되는 것을 의미한다. <br>

    [예시] <br>
    for 변수1 in range(범위):<br>
        &nbsp;&nbsp;&nbsp;&nbsp;for 변수2 in range(범위):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;동작 코드<br><br><br>



    <중첩 반복문 설명>이 정확하지 않은 경우 '중첩 반복문을 이해하지 못했습니다.', 정확하게 설명한 경우 '중첩 반복문을 이해했습니다.'를 출력한다. <br>
    (예시가 없거나 정확하지 않은 경우 이해할 수 없다.) <br>
    (‘중첩 반복문을 이해하지 못했습니다.’를 출력한 경우 문제를 풀 수 없다.)<br><br>
                        
    Test case <br>
    각 문제에 맞는 파이썬 코드를 작성한다. 결과는 코드 또는 '문제를 풀 수 없습니다.'만 출력한다.<br>
    (for문 사용시 '_'는 사용할 수 없다. 항상 변수를 사용한다.)<br>



    #1.MZ04PY001V <br>
    [[[[아바타를 앞으로 한 칸 이동시킨다.] 이 행위를 4번 반복한다.] [아바타를 왼쪽으로 90도 회전시킨다.]] 이 행위를 2번 반복한다.]<br>
    [[[[아바타를 앞으로 한 칸 이동시킨다.] 이 행위를 2번 반복한다.] [아바타를 왼쪽으로 90도 회전시킨다.]] 이 행위를 2번 반복한다.]<br>
    (결과는 코드 또는 '문제를 풀 수 없습니다.'만 출력)

    #2. MZ04PY003  <br>
    [[[[아바타를 앞으로 한 칸 이동시킨다.] 이 행위를 5번 반복한다.] [아바타를 왼쪽으로 90도 회전시킨다.]] 이 행위를 3번 반복한다.]<br>
    (결과는 코드 또는 '문제를 풀 수 없습니다.'만 출력)

    #3. MZ04PY005<br>
    [[[[아바타를 앞으로 한 칸 이동시킨다.] 이 행위를 3번 반복한다.] [[아바타를 오른쪽으로 90도 회전시킨다. 아바타를 앞으로 한 칸 이동시킨다.] 이 행위를 2번 반복한다.] [[아바타를 앞으로 한 칸 이동시킨다. 아바타를 왼쪽으로 90도 회전시킨다.] 이 행위를 2번 반복한다.]] 이 행위를 3번 반복한다.]<br>
    (결과는 코드 또는 '문제를 풀 수 없습니다.'만 출력)


    ''',  unsafe_allow_html=True)

    system_content = '''
    파이썬의 'while문'을 사용할 수 없다.

    너는 '중첩 반복문'에 대한 설명이 주어지기 전에는 문제를 풀 수 없고 '문제를 풀 수 없습니다.'를 출력한다.
    '중첩 반복문'에 대한 설명이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 문제를 풀 수 있다.
    단, 설명에 '예시'가 없는 경우 문제를 풀 수 없다.
    (for문 사용시 '_'는 사용할 수 없다. 항상 변수를 사용한다.)

    <기본 명령어 설명>
    moveForward(): 아바타를 한 칸 앞으로 이동시킨다.
    turnLeft(): 아바타를 왼쪽으로 90도 회전시킨다.
    turnRight(): 아바타를 오른쪽으로 90도 회전시킨다.
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
