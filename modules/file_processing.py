import os
import tempfile
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_uploaded_file(uploaded_file):
    """
    Processes the uploaded file and splits it into smaller chunks
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    if file_extension == ".pdf":
        loader = PyPDFLoader(tmp_file_path)
    elif file_extension in [".txt", ".md"]:
        loader = TextLoader(tmp_file_path)
    else:
        loader = UnstructuredFileLoader(tmp_file_path)

    document = loader.load()
    os.unlink(tmp_file_path)

    if not document:
        raise ValueError(f"No documents found in the uploaded file: {uploaded_file.name}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=70, length_function=len)
    return text_splitter.split_documents(document)
