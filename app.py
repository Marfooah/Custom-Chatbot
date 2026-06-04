import streamlit as st
import tempfile
import os

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 Excel & TXT Chatbot")

google_api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password"
)

uploaded_files = st.file_uploader(
    "Upload TXT and/or Excel files",
    type=["txt", "xlsx"],
    accept_multiple_files=True
)

if google_api_key and uploaded_files:

    docs = []

    for uploaded_file in uploaded_files:

        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        if suffix == ".txt":
            loader = TextLoader(temp_path)

        elif suffix == ".xlsx":
            loader = UnstructuredExcelLoader(temp_path)

        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        k=3
    )

    prompt_template = PromptTemplate(
        input_variables={"context", "question"},
        template="""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Answer: Provide a clear and concise answer based on the context above, if the context doesn't contain enough information to answer the answer then say so"""
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.5,
        convert_system_message_to_human=True
    )

    def rag(query):
        docs = retriever.invoke(query)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = prompt_template.format(
            context=context,
            question=query
        )

        response = llm.invoke(prompt)

        return response.content

    user_query = st.text_input(
        "Ask a question about your uploaded files:"
    )

    if st.button("Ask") and user_query:

        with st.spinner("Thinking..."):
            answer = rag(user_query)

        st.subheader("Answer")
        st.write(answer)
