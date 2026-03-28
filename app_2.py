import streamlit as st
import tempfile
import os
from rag_pipeline import build_rag_chain

# --- PAGE SETUP ---
st.title("📄 Chat with your PDF")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:

    # --- SAVE FILE TEMPORARILY ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # --- BUILD CHAIN ONCE, SAVE IN SESSION ---
    if "chain" not in st.session_state:
        with st.spinner("Reading and indexing your PDF..."):
            st.session_state.chain = build_rag_chain(tmp_path)
        st.success("Ready! Ask your question below.")

    # --- INIT CHAT HISTORY ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- DISPLAY CHAT HISTORY ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # --- CHAT INPUT ---
    question = st.chat_input("Ask a question about your PDF...")

    if question:
        # Show user message
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # Get and show answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = st.session_state.chain(question)
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # --- CLEANUP ---
    os.remove(tmp_path)