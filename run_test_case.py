import streamlit as st

def run_test_case(test_case, client, gpt_model):
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