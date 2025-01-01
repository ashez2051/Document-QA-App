# Document Q&A App

A Streamlit-based app for question answering with document uploads and RAG (Retrieval-Augmented Generation).

## Features
- Login system
- Document upload and processing
- Knowledge base creation with ChromaDB
- Question answering with OpenAI

## Setup
1. Clone the repository:  https://github.com/ashez2051/LangChain.git

2. Install dependencies: pip install -r requirements.txt

3. Create a `.env` file with your OpenAI API key: OPENAI_API_KEY=your_key OPENAI_BASE_URL=your_url

4. Run the app: streamlit run app.py

## Folder Structure
- `modules/`: Contains modularized code for authentication, file processing, etc.
- `docs/`: Stores ChromaDB files.
