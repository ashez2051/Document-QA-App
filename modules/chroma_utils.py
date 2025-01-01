from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import streamlit as st

def build_chroma_db(documents):
    """
    Builds a Chroma database from the provided documents
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    chroma_db = Chroma.from_documents(documents, embeddings, persist_directory="docs/chroma")
    return chroma_db

def clear_chroma_db():
    """
    Clears the Chroma database and removes it from session state
    """
    if "vectorstore" in st.session_state:
        st.session_state.vectorstore = None