import streamlit as st

def handler_user_input(prompt, client, gpt_model):
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