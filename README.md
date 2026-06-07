# RAG Chatbot for TXT and Excel Files

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot built using LangChain, FAISS, Google Gemini, and Streamlit.

The chatbot allows users to upload TXT and Excel (.xlsx) files and ask questions about the contents of those files. Instead of searching the internet, the chatbot retrieves relevant information from the uploaded documents and uses Google's Gemini model to generate answers.

---

🚀 Live Demo: https://aidailymoodtracker.streamlit.app/

## 📸 Application Preview

### Home Page
<img width="2950" height="1156" alt="image" src="https://github.com/user-attachments/assets/e8623853-3f6b-499b-a779-541e99037a29" />

### Files Uploaded Successfully
<img width="2950" height="1664" alt="image" src="https://github.com/user-attachments/assets/65797b2f-fb6e-46ed-8d04-6bce0a3d33b4" />

### Queries regarding Uploaded files
<img width="2950" height="1664" alt="image" src="https://github.com/user-attachments/assets/2f74cd23-d6ea-4a91-905d-b6a5b9d29cb0" />
<img width="2950" height="670" alt="image" src="https://github.com/user-attachments/assets/fa390820-a0c1-49a0-9628-b25b07ecf00b" />

---

## Features

* Upload TXT files
* Upload Excel (.xlsx) files
* Process multiple files simultaneously
* Document chunking using LangChain
* Semantic search using Gemini Embeddings
* Vector storage using FAISS
* Question Answering using Gemini 2.5 Flash
* Streamlit web interface

---

## Technologies Used

* Python
* Streamlit
* LangChain
* Google Gemini API
* FAISS
* Pandas
* OpenPyXL

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

After running the command, Streamlit will open a local web application in your browser.

---

## How to Use

1. Launch the Streamlit application.
2. Enter your Google Gemini API Key.
3. Upload one or more TXT and/or Excel files.
4. Enter a question related to the uploaded documents.
5. Click the **Ask** button.
6. The chatbot will retrieve relevant information from the uploaded files and generate an answer.

---

## Retrieval-Augmented Generation (RAG) Workflow

1. Documents are uploaded by the user.
2. TXT and Excel files are loaded into LangChain.
3. Documents are split into smaller chunks.
4. Gemini Embeddings convert the chunks into vector representations.
5. FAISS stores the vectors for efficient retrieval.
6. User questions are converted into embeddings.
7. The most relevant document chunks are retrieved.
8. Gemini 2.5 Flash generates a response using the retrieved context.

---

## Dependencies

The project uses the following libraries:

* streamlit
* langchain-community
* unstructured[xlsx]
* langchain-text-splitters
* langchain-google-genai
* faiss-cpu
* pandas
* openpyxl

---

## API Key Setup

This project requires a Google Gemini API key.

You can obtain one from Google AI Studio.

When running the application:

1. Enter your Gemini API key in the provided input field.
2. The key is used only during the current session.
3. Do not share or publish your API key.

---

## Limitations

* Supports TXT files only for text documents.
* Supports Excel files in .xlsx format.
* Requires an active internet connection to access Gemini models.
* Answer quality depends on the quality and completeness of uploaded documents.

---

## Future Improvements

* PDF support
* Word document support
* Conversation memory
* Chat history
* Persistent vector database
* Deployment on Streamlit Community Cloud

The Google Stitch UI design is included as a ZIP file due to multiple nested folders and duplicate filenames within the export structure. Please download and extract the ZIP to view the full design.
