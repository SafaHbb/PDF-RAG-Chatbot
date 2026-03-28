# PDF RAG Chatbot

Chat with any PDF using a local AI — no API key needed.

## What it does
Upload a PDF, ask questions about it, and get answers from the AI.
Everything runs on your own machine using Ollama.

## How it works
1. You upload a PDF
2. The app breaks it into small chunks and stores them
3. When you ask a question, it finds the most relevant chunks
4. The local AI (llama3.2) reads those chunks and answers

## Tools used
- Ollama — runs the AI locally on your machine
- LangChain — connects all the pieces together
- FAISS — searches for relevant text chunks
- HuggingFace — turns text into vectors (also local)
- Streamlit — the chat interface

## How to run it
1. Install Ollama from https://ollama.com and run:
   ollama pull llama3.2

2. Install Python libraries:
   pip install -r requirements.txt

3. Start the app:
   streamlit run app.py

4. Open http://localhost:8501 in your browser

## Limitations
- Works best with text-based PDFs
- Scanned or image-only PDFs are not supported yet
