import streamlit as st
from utils.api import ask_question
import time

def render_chat():
    st.subheader("💬 Chat with your assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # input and response
    user_input = st.chat_input("Type your question...")
    if user_input:
        # Display user message
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Create a placeholder for the assistant's response
        assistant_placeholder = st.empty()
        
        # Show animated typing indicator
        with assistant_placeholder.container():
            with st.chat_message("assistant"):
                typing_container = st.empty()
                for i in range(3):
                    typing_container.markdown("Thinking" + "." * (i+1))
                    time.sleep(0.3)

        # Call API with loading spinner
        with st.spinner("Assistant is processing your question..."):
            response = ask_question(user_input)

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "No response returned.")
            sources = data.get("sources", [])

            # Replace typing indicator with actual response
            with assistant_placeholder.container():
                # Display assistant message
                st.chat_message("assistant").markdown(answer)
                if sources:
                    st.chat_message("assistant").markdown(
                        "📄 **Sources:**\n" + "\n".join([f"- `{s}`" for s in sources])
                    )

            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Add success sound and visual effect
            st.balloons()
        else:
            error_msg = f"Error: {response.text}"
            
            # Replace typing indicator with error
            with assistant_placeholder.container():
                st.chat_message("assistant").error(error_msg)
                
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
