# 📚 PDF Study Assistant — RAG-Based AI Chatbot

> A production-quality AI-powered PDF chatbot built with Python, Streamlit, LangChain, and Groq API.  
> Upload your notes or textbooks — ask questions, get summaries, and generate quizzes instantly.

---

## 🎯 What Is This?

This is a **Retrieval-Augmented Generation (RAG)** application that lets students:

1. Upload one or multiple PDF files (lecture notes, textbooks, papers)
2. Ask questions in natural language
3. Get **accurate, context-only answers** — no hallucination
4. Summarize entire documents in seconds
5. Auto-generate MCQ practice quizzes
6. Identify key topics to study

Built with **CPU-only** support — runs perfectly on 8GB RAM without any GPU.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Chat Interface** | ChatGPT-style conversation with your PDF |
| 📋 **PDF Summarizer** | One-click structured summary of any document |
| 🧪 **Quiz Generator** | Auto-generate 5 MCQ questions for practice |
| 🔑 **Key Topics** | Extract the most important topics to study |
| 📌 **Source Attribution** | See exactly which page/chunk each answer came from |
| 📁 **Multi-PDF Support** | Upload and query multiple PDFs simultaneously |
| 🔒 **No Hallucination** | Strict context-only answering enforced via prompts |
| 💾 **Export Results** | Download summaries and quizzes as text files |
| 🎨 **Modern Dark UI** | Professional, clean interface |

---

## 🧠 How It Works (RAG Pipeline)

```
PDF Upload
    ↓
Text Extraction (PyPDFLoader)
    ↓
Chunking (RecursiveCharacterTextSplitter: 500 chars, 50 overlap)
    ↓
Embedding (all-MiniLM-L6-v2 — CPU-friendly)
    ↓
Storage (ChromaDB — local vector database)
    ↓
User Question → Semantic Search (MMR retrieval, top 3 chunks)
    ↓
Context + Question → Groq API (LLaMA 3 8B)
    ↓
Structured Answer → Displayed in Chat UI
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | LLaMA 3 (8B) via Groq API |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector DB** | ChromaDB |
| **PDF Loading** | LangChain PyPDFLoader |
| **Text Splitting** | RecursiveCharacterTextSplitter |
| **RAG Pipeline** | LangChain |
| **Environment** | python-dotenv |

---

## 📁 Project Structure

```
pdf-chatbot/
├── app.py                  # Main Streamlit application (UI + logic)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file
└── utils/
    ├── __init__.py         # Package marker
    ├── pdf_loader.py       # PDF loading and text extraction
    ├── text_splitter.py    # Document chunking
    ├── embeddings.py       # Sentence transformer model loader
    ├── vector_store.py     # ChromaDB operations (build, load, clear)
    ├── retriever.py        # Semantic search (MMR retrieval)
    ├── groq_client.py      # Groq API client and error handling
    └── prompts.py          # All prompt templates (QA, Summary, Quiz, Topics)
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.9 or higher
- pip
- A free Groq API key (see below)

### Step 1: Clone / Download the project

```bash
# If using git:
git clone https://github.com/yourusername/pdf-chatbot.git
cd pdf-chatbot

# Or just unzip and cd into the folder
```

### Step 2: Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

> ⏱️ First install downloads ~500MB (sentence-transformers model). Subsequent runs are fast.

### Step 4: Set up your Groq API key

```bash
# Copy the example file
cp .env.example .env
```

Now open `.env` in any text editor and replace `your_groq_api_key_here`:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Get a FREE Groq API key:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Click **"Create API Key"**
4. Copy and paste into your `.env` file

### Step 5: Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## 🚀 Usage Guide

### Basic Chat
1. Upload a PDF using the **sidebar uploader**
2. Click **"⚡ Process PDFs"** — wait ~30 seconds for embedding
3. Go to the **💬 Chat** tab
4. Type any question and press **Send 🚀**

### Generate a Summary
1. After processing your PDF, go to the **📋 Summarize** tab
2. Click **"🔍 Generate Summary"**
3. Download the summary with the **💾 Download** button

### Generate a Quiz
1. Go to the **🧪 Generate Quiz** tab
2. Optionally type a specific topic (e.g., *"neural networks"*)
3. Click **"🎯 Generate Quiz"**
4. Use the 5 MCQs to test your knowledge

### Extract Key Topics
1. Go to the **🔑 Key Topics** tab
2. Click **"🔍 Extract Key Topics"**
3. Use the topic list as your study guide

---

## 💡 Example Queries

```
"Explain machine learning in simple words"
"What is the difference between RAM and ROM?"
"List all the key formulas in Chapter 4"
"What are the three laws of motion?"
"Define recursion with an example"
"Summarize the chapter on photosynthesis"
"What are the advantages of neural networks?"
"Who invented the telephone according to this document?"
```

---

## 📸 Screenshots

> *Add screenshots here after running the app*

| Upload & Process | Chat Interface |
|---|---|
| ![Upload]() | ![Chat]() |

| Quiz Generator | Key Topics |
|---|---|
| ![Quiz]() | ![Topics]() |

---

## ⚡ Performance Notes

- **First run:** ~30-60 seconds (downloads embedding model + processes PDF)
- **Subsequent questions:** ~2-5 seconds each
- **RAM usage:** ~1-2 GB (safe for 8GB systems)
- **GPU:** Not required — fully CPU-based

### Optimization Settings (in code)
```python
chunk_size    = 500   # Characters per chunk
chunk_overlap = 50    # Overlap between chunks
top_k         = 3     # Chunks retrieved per query
temperature   = 0.2   # Low = more deterministic/factual
max_tokens    = 1024  # Response length cap
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `GROQ_API_KEY not set` | Check your `.env` file has the key |
| `No text extracted` | PDF may be scanned/image-based — use OCR first |
| `Rate limit error` | Wait 10-15 seconds and retry |
| `Slow processing` | Normal on first run (model download). Faster after. |
| `Import error` | Run `pip install -r requirements.txt` again |
| `Port in use` | Run `streamlit run app.py --server.port 8502` |

---

## 🔮 Future Improvements

- [ ] **OCR support** for scanned PDFs (pytesseract)
- [ ] **Multi-language support** for non-English documents
- [ ] **Flashcard generator** (Q&A pairs for spaced repetition)
- [ ] **Mind map generator** from document topics
- [ ] **Chat export** to PDF or Word
- [ ] **Document comparison** (ask questions across multiple PDFs)
- [ ] **Semantic search slider** (adjust number of retrieved chunks)
- [ ] **Voice input** for questions (speech-to-text)
- [ ] **Google Drive integration** for direct PDF import
- [ ] **Authentication** for multi-user deployment

---

## 📜 License

MIT License — Free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Blazing fast LLM inference
- [LangChain](https://langchain.com) — RAG pipeline framework
- [ChromaDB](https://trychroma.com) — Local vector database
- [Streamlit](https://streamlit.io) — Python web UI framework
- [Sentence Transformers](https://sbert.net) — CPU-friendly embeddings

---

*Built with ❤️ for students who want to study smarter, not harder.*
