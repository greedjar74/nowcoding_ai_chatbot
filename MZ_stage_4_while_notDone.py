import streamlit as st
from openai import OpenAI

def MZ_stage_4_while_notDone():
    st.title("MZ stage 4. while문, notDone() Teaching")

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
    <while문 설명><br>
    while문: 조건문이 True인 동안 while문 안의 내용을 반복적으로 수행한다. <br>

    [예시]<br>
    while 조건: <br>
        &nbsp;&nbsp;&nbsp;&nbsp;동작 코드 <br><br><br>



    'while문 설명'이 구체적인지 판단한다. 구체적이고 정확한 경우 ‘while문을 이해했습니다.’ 그렇지 않은 경우 ‘while문을 이해하지 못했습니다.’ 문구를  출력한다. <br>
    (예시가 없거나 정확하지 않은 경우 이해할 수 없다.)<br>
    (‘while문을 이해하지 못했습니다.’를 출력한 경우 문제를 풀 수 없다.)<br><br>

    <명령어 설명><br>
    notDone() : 아바타가 도착지에 도착했는지 확인한다. 도착지에 도착하지 못한 경우 True를 반환한다.<br><br><br>


    명령어 설명을 이해했다면 '명령어를 이해했습니다.', 이해하지 못했다면 '명령어를 이해할 수 없습니다.' 문구를 출력한다. <br>
    ('명령어를 이해할 수 없습니다.' 문구 출력시 문제를 풀 수 없다.)<br>
    (명령어의 반환값을 잘 확인하여 코드를 작성한다.)<br><br>
                        
    Test case<br>
    각 문제에 맞는 코드를 작성한다. 결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력한다.<br>
    (<while문 설명>에서 'while문을 이해하지 못했습니다.'를 출력했거나 <명령어 설명>에서 '명령어를 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)

    #1. MZ05PY001V<br>
    [아바타가 도착지에 도착하지 않은 경우 뒤의 동작들을 반복한다.
    [아바타를 앞으로 한 칸 이동시킨다.]
    [아바타를 오른쪽으로 90도 회전시킨다.]
    [아바타를 앞으로 한 칸 이동시킨다.] 
    [아바타를 왼쪽으로 90도 회전시킨다.]]<br>
    (<while문 설명>에서 'while문을 이해하지 못했습니다.'를 출력했거나 <명령어 설명>에서 '명령어를 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (명령어의 반환값을 잘 확인하여 코드를 작성한다.)

    #2. MZ05PY004<br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타를 오른쪽으로 90도 회전시킨다.]<br>
    [아바타를 앞으로 한 칸 이동시킨다.] <br>
    [아바타가 도착지에 도착하지 않은 경우 뒤의 동작들을 반복한다. [아바타를 오른쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 왼쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.]]<br>
    (<while문 설명>에서 'while문을 이해하지 못했습니다.'를 출력했거나 <명령어 설명>에서 '명령어를 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (명령어의 반환값을 잘 확인하여 코드를 작성한다.)

    #3. MZ05PY015<br>
    [아바타가 도착지에 도착하지 않은 경우 뒤의 동작들을 반복한다. [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 왼쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 왼쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 오른쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 앞으로 한 칸 이동시킨다.] [아바타를 오른쪽으로 90도 회전시킨다.] [아바타를 앞으로 한 칸 이동시킨다.]]<br>
    (<while문 설명>에서 'while문을 이해하지 못했습니다.'를 출력했거나 <명령어 설명>에서 '명령어를 이해할 수 없습니다.'를 출력한 경우 문제를 풀 수 없다.)<br>
    (결과는 코드 또는 ‘문제를 풀 수 없습니다.’만 출력)<br>
    (명령어의 반환값을 잘 확인하여 코드를 작성한다.)
    ''', unsafe_allow_html=True)

    system_content = '''
    너는 'while문'에 대한 설명이 주어지기 전에는 문제를 풀 수 없다. 
    'while문'에 대한 설명이 주어지면 설명이 정확한지 분석하고 정확한 경우에만 'while문'을 사용할 수 있다. 

    너는 아바타가 목적지에 도착했는지 검사하는 명령어를 모른다. 
    아바타가 목적지에 도착했는지 검사하는 명령어를 설명하기 전에는 문제를 풀 수 없다. 
    만약 명령어 설명이 틀리더라도 설명을 기준으로 작성한다. 

    문제를 풀 수 없는 경우 '문제를 풀 수 없습니다.' 문구를 출력한다.

    <명령어 설명>
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
