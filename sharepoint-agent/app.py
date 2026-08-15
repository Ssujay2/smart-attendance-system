import streamlit as st

from agent import ask_agent


st.set_page_config(
    page_title="SharePoint AI Agent",
    page_icon="📚",
    layout="centered"
)


st.title("📚 SharePoint AI Agent")

st.write(
    "Ask questions about documents stored in the SharePoint document repository."
)


question = st.text_input(
    "Ask a question",
    placeholder="Example: How many paid leaves do employees get?"
)


if st.button("Ask Agent"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching documents and generating answer..."):

            try:

                answer = ask_agent(question)

                st.subheader("Answer")

                st.write(answer)

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )