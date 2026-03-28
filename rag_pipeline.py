from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

def build_rag_chain(pdf_path):

    # --- STEP A: Load the PDF ---
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    # --- STEP B: Split into chunks ---
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # --- STEP C: Embed and store in FAISS ---
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    # --- STEP D: Connect to Ollama ---
    llm = ChatOllama(model="llama3.2", temperature=0)

    # --- STEP E: Build a simple chain manually ---
    def chain(question):
        # docs = retriever.get_relevant_documents(question)
        docs = retriever.invoke(question)

        context = "\n\n".join([d.page_content for d in docs])
        prompt = f"Answer based on this context only:\n\n{context}\n\nQuestion: {question}"
        response = llm.invoke(prompt)
        return response.content

    return chain