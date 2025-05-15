import streamlit as st
from openai import OpenAI

def NP_stage_5():
    st.title("NP stage 5. 대각선 패턴 Teaching")

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

    st.sidebar.markdown("# 입력 prompt")
    st.sidebar.markdown('''
    <패턴 설명> <br>
    패턴: 배열에서 1의 값을 가지는 위치들을 오름차순 정렬했을 때 행 값과 열 값이 모두 1씩 증가한다.

    [예시]<br>
    [[1, 0, 0, 0],<br>
    [0, 1, 0, 0],<br>
    [0, 0, 1, 0],<br>
    [0, 0, 0, 1]]<br><br><br>



    패턴을 이해했다면 ‘패턴을 이해했습니다.’ 이해하지 못했다면 ‘패턴을 이해하지 못했습니다.’ 문구 출력 <br>
    단, 예시가 없거나 설명에 부합하지 않는 경우 패턴을 이해할 수 없다.<br>
    (‘패턴을 이해하지 못했습니다.’ 문구 출력시 문제를 풀 수 없다.)<br><br>

    Test case <br>
    배열에 패턴이 존재하는지 파악한다. 결과는 True, False 또는 ‘문제를 풀 수 없습니다.’만 출력<br>
    (<패턴 설명>에서 ‘패턴을 이해하지 못했습니다.’ 문구를 출력한 경우 문제를 풀 수 없다.)

    #1. [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]<br>
    (결과는 True, False 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (<패턴 설명>에서 ‘패턴을 이해하지 못했습니다.’ 문구를 출력한 경우 문제를 풀 수 없다.)

    #2. [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]] <br>
    (결과는 True, False 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (<패턴 설명>에서 ‘패턴을 이해하지 못했습니다.’ 문구를 출력한 경우 문제를 풀 수 없다.)


    #3. [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]<br>
    (결과는 True, False 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (<패턴 설명>에서 ‘패턴을 이해하지 못했습니다.’ 문구를 출력한 경우 문제를 풀 수 없다.)

    #4. [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0]]<br>
    (결과는 True, False 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (<패턴 설명>에서 ‘패턴을 이해하지 못했습니다.’ 문구를 출력한 경우 문제를 풀 수 없다.)
    ''', unsafe_allow_html=True)
    
    system_content = '''
    배열이 주어지면 배열 내부에 '패턴'이 존재하는지 파악한다.
    '패턴'에 대한 설명이 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.
    '패턴'에 대한 설명이 주어지면 패턴이 있는지 파악하여 결과를 출력한다.

    단,'패턴' 설명에 주어진 예시를 분석하여 설명과 다른 경우 문제를 풀 수 없다.

    (패턴이 있는 경우 True, 패턴이 없는 경우 False)
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