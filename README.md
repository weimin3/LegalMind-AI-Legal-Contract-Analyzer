# LegalMind: AI Legal Contract Analyzer

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)

LegalMind is an AI-powered web application designed to simplify legal contract analysis. Upload PDF or TXT contract files, receive automatic structured summaries highlighting key parties, obligations, risks, and more, and engage in interactive Q&A conversations about the contract content. Built with local AI models for privacy and efficiency.

## ✨ Features

- **File Upload Support**: Accepts PDF and TXT contract files
- **Automatic Contract Summarization**: Generates structured summaries including:
  - Parties involved
  - Contract type
  - Key obligations
  - Important dates
  - Financial terms
  - Termination conditions
  - Risk assessment (High/Medium/Low risk clauses)
- **Interactive Chat Interface**: Ask questions about the contract and get AI-powered responses
- **Vector-Based Search**: Uses ChromaDB for efficient document retrieval
- **Local AI Models**: Runs entirely on your machine using Ollama for privacy
- **Session Management**: Maintains chat history per contract
- **Duplicate Detection**: Uses MD5 hashing to avoid reprocessing identical files

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Framework**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Ollama (nomic-embed-text)
- **LLM**: Ollama (llama3.2)

## 🚀 Installation

### Prerequisites

- Python 3.11

### Steps

1. **Clone the repository:**

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install streamlit PyPDF2 langchain langchain-chroma langchain-ollama langchain-community
   ```

4. **Install and setup Ollama models:**
   ```bash
   # Install Ollama (if not already installed)
   # Download from https://ollama.ai/

   # Pull required models
   ollama pull nomic-embed-text
   ollama pull llama3.2
   ```

## 🎯 Usage

1. **Start Ollama service (in a separate terminal):**
   ```bash
   ollama serve
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Use the app:**
   - Upload a contract file (PDF or TXT) in the left panel
   - Click "Analyze Contract" to process and generate summary
   - View the automatic summary
   - Ask questions about the contract in the right panel chat interface

## 📁 Project Structure

```
LegalMind-AI-Legal-Contract-Analyzer/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration settings
├── knowledge_base.py         # Knowledge base service for document processing
├── rag.py                    # RAG (Retrieval-Augmented Generation) service
├── vector_store.py           # Vector store utilities
├── file_history_store.py     # Chat history management
├── md5_util.py              # MD5 hashing utilities
├── md5.text                 # MD5 hash storage
├── data/                    # Sample contract files(Contract Understanding Atticus Dataset:(https://www.atticusprojectai.org/cuad))
├── chroma_db/               # ChromaDB vector database storage
├── chat_history/            # Chat conversation history
└── README.md                # This file
```

## 🔧 Configuration

Key configuration options in `config.py`:

- **Database Settings**: ChromaDB persistence directory and collection names
- **Text Splitting**: Chunk size, overlap, and separators for document processing
- **Model Configuration**: Embedding and chat model names
- **Similarity Threshold**: Number of similar documents to retrieve
- **Paths**: Chat history and MD5 storage locations

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- Report bugs or issues
- Suggest new features
- Submit pull requests

## ⚠️ Disclaimer

This tool is for informational purposes only and does not constitute legal advice. Always consult with qualified legal professionals for contract analysis and interpretation.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI framework
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Ollama](https://ollama.ai) for local AI models
- [Streamlit](https://streamlit.io/) for the web interface
