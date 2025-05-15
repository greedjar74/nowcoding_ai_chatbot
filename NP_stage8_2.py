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

    st.sidebar.markdown("# 입력 prompt")
    st.sidebar.markdown('''
    <명령어 설명> <br>
    erase(x, y): n by n 크기의 행렬 x행, y열 위치의 값에서 1을 감소시킨다. <br><br><br>

    <명령어 설명>이 구체적인 경우  ‘명령어를 이해했습니다.’, 구체적이지 않은 경우 ‘명령어를 이해할 수 없습니다.’ 문구 출력<br>
    명령어는 정의되어 있으므로 따로 정의할 필요 없다.<br><br>

    <문제 설명> <br>
    0이상의 값이 저장된 배열이 주어질 때 모든 값을 0으로 만드는 파이썬 코드를 만든다. <br>
    x, y 위치의 값을 감소시키기 위해서는 정해진 명령어만 사용할 수 있다. <br><br><br>

    <문제 설명>이 이해된다면  ‘문제 설명을 이해했습니다.’, 이해할 수 없는 경우 ‘문제 설명을 이해할 수 없습니다.’ 문구 출력<br>
    명령어는 정의되어 있으므로 따로 정의할 필요 없다. <br><br>

    <제약조건 설명><br>
    for문을 코드에 한 번 명시할 때마다 반복문 사용 횟수를 1 증가시킨다. <br>
    erase 명령어를 코드에 한 번 명시할 때마다 커맨드 사용 횟수를 1 증가시킨다. <br>
    단, 반복문에 의한 중복 호출은 무시한다. <br><br><br>

    설명이 구체적인 경우 ‘제약조건을 이해했습니다.’, 구체적으로 작성되지 않은 경우 ‘제약조건을 이해할 수 없습니다.’ 문구를 출력한다. <br>
    (‘제약조건을 이해할 수 없습니다.’ 출력시 문제를 풀 수 없다.)<br><br>

    <범위설정 설명> <br>
    range(start, end, term) : ‘start’부터 ‘end-1’까지 ‘term’ 간격으로 증가한다. 

    [예시]<br>
    for i in range(start, end, term): <br>
        &nbsp;&nbsp;&nbsp;&nbsp;동작코드 <br><br><br>

    <범위설정 설명>이 정확한 경우 '범위설정 설명을 이해했습니다.', 정확하지 않은 경우 '범위설정 설명을 이해하지 못했습니다.' 문구를 출력한다. <br>
    ([예시]가 없거나 정확하지 않은 경우 이해할 수 없다.) <br>
    (설명에서 range에 입력한 'end'보다 1 작은 값까지 수행된다는 설명이 정확히 표현되었는지 확인한다.)<br><br>

    <패턴 설명> <br>
    패턴: 배열에서 1의 값을 가지는 위치들을 오름차순 정렬한다. 행, 열 값이 가장 작은 위치를 기준으로 n by n 영역이 모두 1이다.

    [예시]<br>
    [[1, 1, 1, 1], <br>
    [1, 1, 1, 1], <br>
    [1, 1, 1, 1], <br>
    [1, 1, 1, 1]]<br><br><br>


    패턴을 이해했다면 ‘패턴을 이해했습니다.’ 이해하지 못했다면 ‘패턴을 이해하지 못했습니다.’ 문구 출력<br>
    단, 예시가 없거나 설명에 부합하지 않는 경우 패턴을 이해할 수 없다.<br><br>
                        
    Test case <br>
    <문제설명>에 해당하는 파이썬 코드를 작성한다. 결과는 파이썬 코드 또는 '문제를 풀 수 없습니다.'만 출력<br>
    (코드를 생성하기 전 <사전 설정>을 다시 확인하고 문제를 해결한다.)<br>
    (배열, 명령어는 따로 정의할 필요 없다.)

    \- <명령어 설명>, <문제 설명>, <제약조건 설명>, <범위설정 설명> 중 하나라도 '이해하지 못했습니다.'를 출력한 경우 문제를 풀 수 없다.<br>

    \- <패턴 설명>이 없거나 '패턴을 이해하지 못했습니다.' 문구 출력시 'for문'을 사용할 수 없다. 1이 저장된 모든 위치를 찾고 각각 명령어를 적용하여 파이썬 코드를 작성한다. (제약조건은 무시한다.)<br>
                        
    \- <패턴 설명>이 주어진 경우 문제의 배열에 패턴이 존재하는지 확인한다. <br>
    &nbsp;&nbsp;패턴이 존재하는 경우 제약조건을 만족하는 코드를 작성한다. <br>
    &nbsp;&nbsp;패턴이 존재하지 않는 경우 'for문'을 사용할 수 없다. 1이 저장된 모든 위치를 찾고 각각 명령어를 적용하여 파이썬 코드를 작성한다. (제약조건은 무시한다.)<br>

    # NP08PY002 <br>
    제약조건: 반복문 2개, 커맨드 1개 

    [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], <br>
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], <br>
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], <br>
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], <br>
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], <br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], <br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], <br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], <br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], <br>
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ''', unsafe_allow_html=True)
    
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