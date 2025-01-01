import streamlit as st
import os
from dotenv import load_dotenv
from modules.auth import verify_login
from modules.file_processing import process_uploaded_file
from modules.chroma_utils import build_chroma_db, clear_chroma_db
from modules.llm_utils import initialize_openai
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

st.set_page_config(page_title="Document Q&A", layout="centered")

# Login Section
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login to Document Q&A App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")
else:
    # Main Application Section
    st.title("Document Question Answering with OpenAI and RAG")
    st.sidebar.header("Upload your document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt", "md"])

    if uploaded_file:
        st.sidebar.success("File uploaded successfully!")
        documents = process_uploaded_file(uploaded_file)
        st.write("### Document content successfully loaded!")

        if st.button("Build Knowledge Base"):
            with st.spinner("Processing the document and building the knowledge base..."):
                vectorstore = build_chroma_db(documents)
                retriever = vectorstore.as_retriever()
                st.session_state.retriever = retriever
                st.session_state.vectorstore = vectorstore
                st.session_state.memory = ConversationBufferMemory(k=5, memory_key="chat_history", return_messages=True)
                st.success("Knowledge base is ready!")

    if "retriever" in st.session_state:
        question = st.text_input("Enter your question:")
        if st.button("Get Answer") and question:
            with st.spinner("Fetching answer..."):
                llm = initialize_openai(OPENAI_API_KEY, OPENAI_BASE_URL)

                # Define the custom prompt
                system_prompt = (
                    "Use the given context to answer the question. "
                    "If you don't know the answer, say you don't know. "
                    "Use three sentences maximum and keep the answer concise. "
                    "Context: {context}"
                )
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ]
                )

                # Create a chain for combining documents and retrieving answers
                question_answer_chain = create_stuff_documents_chain(llm, prompt)
                chain = create_retrieval_chain(st.session_state.retriever, question_answer_chain)

                # Run the chain with user input
                result = chain.invoke({"input": question})
                answer = result["answer"]
                sources = [doc.metadata.get("source") for doc in result.get("context", [])]
                unique_sources = set(sources)

                st.write("**Answer:**", answer)
                st.write("**Source Documents:**", unique_sources)

    if st.button("Clear Session"):
        clear_chroma_db()
        st.session_state.clear()
        st.success("Session cleared!")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
