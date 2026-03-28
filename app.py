import streamlit as st
import tempfile
import os
from rag_pipeline import build_rag_chain

# --- PAGE SETUP ---
st.title("📄 Chat with your PDF")
st.write("Upload a PDF and ask questions about it.")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:

    # --- SAVE FILE TEMPORARILY ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # --- BUILD THE RAG CHAIN ---
    with st.spinner("Reading and indexing your PDF..."):
        chain = build_rag_chain(tmp_path)

    st.success("Ready! Ask your question below.")

    # --- QUESTION INPUT ---
    question = st.text_input("Your question:")

    if question:
        with st.spinner("Thinking..."):
            result = chain(question)
            st.write("**Answer:**", result)

    # --- CLEANUP ---
    os.remove(tmp_path)