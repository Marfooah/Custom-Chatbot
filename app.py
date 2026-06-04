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

st.set_page_config(
    page_title="Document Intelligence AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
# 🚀 Document Intelligence AI

Ask questions from your TXT and Excel files in seconds.

Upload your documents, chat with your data, and get instant AI-powered insights.
""")

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
}

[data-testid="stSidebar"] {
    background-color: #161b22;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 RAG Chatbot")

    st.markdown("""
    ### Supported Files
    - TXT
    - XLSX

    ### Powered By
    - Gemini 2.5 Flash
    - LangChain
    - FAISS
    """)

with st.container():
    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload TXT and Excel files",
        type=["txt", "xlsx"],
        accept_multiple_files=True
    )

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")

google_api_key = st.secrets["GOOGLE_API_KEY"]

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

    user_query = st.chat_input(
    "Ask something about your documents..."
)

    if user_query:

        with st.spinner("Thinking..."):
            answer = rag(user_query)

        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            st.write(answer)
