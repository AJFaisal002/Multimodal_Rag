# 📄 Multimodal RAG — Chat with PDF

A production-ready **Multimodal Retrieval-Augmented Generation (RAG)** system that enables users to chat with PDF documents using both **text and images** as knowledge sources.

Built using modern LLM architecture and vector retrieval for grounded, source-aware question answering.

---

## 🚀 Features

- 📑 Extracts structured text from PDFs
- 🖼 Extracts and processes embedded images
- ✂ Intelligent chunking of document content
- 🤖 Text summarization using OpenAI models
- 🔎 Multimodal semantic retrieval (text + images)
- 💬 Conversational chat interface (Streamlit)
- 📌 Source citation (page-level)
- 🧠 Vector search powered by ChromaDB
- 🔐 Environment-safe API key management

---

## 🏗 Architecture Overview

PDF → Parsing → Text & Image Extraction
→ Summarization
→ Embedding
→ Chroma Vector Store
→ Retriever
→ OpenAI LLM
→ Grounded Answer with Sources


### Core Components

- **Parser** → Extracts text + images using PyMuPDF
- **Summarizer** → Generates semantic summaries
- **Vector Store** → Stores embeddings using ChromaDB
- **Retriever** → Fetches relevant chunks
- **RAG Chain** → Combines retrieved context with LLM
- **Streamlit UI** → Interactive chat application

---

## 🛠 Tech Stack

- Python 3.10
- OpenAI API (GPT-4o-mini)
- ChromaDB
- LangChain
- Streamlit
- PyMuPDF
- Pillow

---

## 📂 Project Structure


multimodal-rag/
│
├── app_streamlit.py # Main Streamlit application
├── app.py # CLI version (optional)
├── config.py # Configuration settings
├── requirements.txt
│
├── src/
│ ├── parser.py
│ ├── summarizer.py
│ ├── vectorstore.py
│ ├── retriever.py
│ └── rag_chain.py
│
├── utils/
│ └── image_utils.py
│
└── data/


---

## ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/multimodal-rag.git
cd multimodal-rag
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Create Environment File

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here

⚠ Never commit .env to GitHub.

▶ Running the Application
py -3.10 -m streamlit run app_streamlit.py

Then open:

http://localhost:8501

Upload a PDF and start chatting.

🧠 How It Works

PDF is uploaded

Text and images are extracted

Content is chunked and summarized

Embeddings are generated

Stored in ChromaDB vector store

User query retrieves relevant chunks

LLM generates grounded response

Source pages are displayed

🔍 Example Use Cases

Academic paper Q&A

Research document exploration

Legal document review

Technical report summarization

Multimodal meme analysis

Content moderation research

📈 Future Improvements

Streaming responses

Confidence scoring

Multi-document support

Cloud deployment

Docker containerization

Persistent user sessions

🎥 Demo

See Demo.mp4 in repository for application walkthrough.

👨‍💻 Authors

Adnan Faisal
Shiti Chowdhury
Department of Computer Science and Engineering
Chittagong University of Engineering and Technology

📜 License

This project is intended for academic and research purposes.
