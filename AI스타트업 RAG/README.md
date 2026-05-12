# AI Startup RAG Chatbot 🤖

A Retrieval Augmented Generation (RAG) chatbot system built with Python, Flask, and LangChain. Designed to answer questions about AI startup materials from a knowledge base of course notes, wiki documentation, and index files.

## Features

✅ **RAG System** - Retrieves relevant documents and generates accurate answers  
✅ **Web Interface** - Beautiful, responsive chat UI  
✅ **API Endpoints** - RESTful API for integration  
✅ **Vector Database** - Persistent Chroma vector store for fast retrieval  
✅ **Multiple Source Types** - Supports .md, .txt, and .pdf files  
✅ **Source Attribution** - Shows relevant documents for each answer  
✅ **Cloud Ready** - Docker-ready for deployment  

## Architecture

```
┌─────────────────────────────────────────┐
│        Web Interface (HTML/CSS/JS)      │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Flask Web Application (app.py)        │
│   - /api/chat - Main chat endpoint      │
│   - /api/rebuild - Rebuild vector store │
│   - /api/health - Health check          │
│   - /api/stats - System statistics      │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   RAG System (rag_chatbot.py)           │
│   - Document Loading & Processing      │
│   - Vector Store Management            │
│   - Query Processing                   │
│   - LLM Integration                    │
└────────────┬────────────────────────────┘
             │
┌────────────▼───────────────────┬────────┐
│   Chroma Vector Database       │ OpenAI│
│   (Persistent Storage)         │ LLM   │
└────────────────────────────────┴────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key (for ChatGPT models)
- pip (Python package manager)

### Installation

1. **Clone/Download the project**
   ```bash
   cd AI스타트업\ RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

4. **Add your OpenAI API Key to `.env`**
   ```
   OPENAI_API_KEY=sk-...
   ```

### Running Locally

**Option 1: Flask Development Server**
```bash
python app.py
```
Then open your browser to `http://localhost:5000`

**Option 2: With Gunicorn (Production-like)**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option 3: Test RAG System Directly**
```bash
python rag_chatbot.py
```
This runs sample queries to test the RAG system without the web interface.

## Project Structure

```
AI스타트업 RAG/
├── app.py                      # Flask web application
├── rag_chatbot.py             # Core RAG system
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .dockerignore             # Docker ignore file
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker compose config
├── templates/
│   └── index.html           # Web UI
├── knowledge_base/          # Your course materials (TO BE ADDED)
│   ├── raw/                 # Raw notes
│   ├── wiki/                # Wiki documentation
│   └── index.md             # Master index
├── chroma_db/               # Vector database (created automatically)
└── README.md                # This file
```

## Knowledge Base Setup

The RAG system expects your course materials in the `knowledge_base` directory:

### Directory Structure
```
knowledge_base/
├── raw/
│   ├── lecture_01.md
│   ├── lecture_02.md
│   └── ...
├── wiki/
│   ├── concepts.md
│   ├── tools.md
│   └── ...
└── index.md              # Master index
```

### Supported File Formats
- **Markdown** (.md) - Recommended
- **Plain Text** (.txt)
- **PDF** (.pdf)

### Adding Documents

1. **Place your files** in `knowledge_base/` subdirectories
2. **Run the rebuild** to update the vector store:
   ```bash
   curl -X POST http://localhost:5000/api/rebuild
   ```
   Or programmatically:
   ```python
   rag = AIStartupRAG()
   rag.build_vectorstore()
   ```

3. **Chat** with your knowledge base!

## API Endpoints

### Chat Endpoint
```
POST /api/chat
Content-Type: application/json

{
  "message": "What are the key characteristics of an AI startup?"
}

Response:
{
  "answer": "An AI startup is a company...",
  "sources": [
    {
      "title": "AI Startup Fundamentals",
      "excerpt": "An AI startup is a company that uses artificial intelligence..."
    }
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Health Check
```
GET /api/health

Response:
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00",
  "rag_initialized": true
}
```

### System Statistics
```
GET /api/stats

Response:
{
  "model": "gpt-3.5-turbo",
  "vector_store": "./chroma_db",
  "embedding_model": "OpenAI",
  "status": "Ready"
}
```

### Rebuild Vector Store
```
POST /api/rebuild

Response:
{
  "status": "success",
  "message": "Vector store rebuilt successfully"
}
```

## Configuration

Set environment variables in `.env`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-3.5-turbo          # or gpt-4

# Application Configuration
KNOWLEDGE_DIR=./knowledge_base
CHROMA_DB_DIR=./chroma_db
DEBUG=False
PORT=5000
```

## Deployment

### Using Docker

1. **Build the image**
   ```bash
   docker build -t ai-startup-rag .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 \
     -e OPENAI_API_KEY=sk-... \
     -v $(pwd)/knowledge_base:/app/knowledge_base \
     ai-startup-rag
   ```

### Docker Compose
```bash
docker-compose up
```

### Cloud Deployment Options

#### Heroku
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

#### Google Cloud Run
```bash
gcloud run deploy ai-startup-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...
```

#### AWS Lambda + API Gateway
See the `serverless.yml` configuration for deployment with Serverless Framework.

#### Azure App Service
```bash
az webapp up --name your-app-name --runtime "python:3.10"
```

## Performance Optimization

### Vector Store
- Uses Chroma for fast in-memory retrieval
- Persistent storage for quick loading
- Configurable chunk size (default: 1000 tokens)

### LLM Calls
- Retrieves top 3 documents per query
- Configurable temperature (0.7 by default)
- Response streaming for faster user feedback

### Suggestions
1. **Increase chunk overlap** for better context
2. **Adjust k in retriever** for more/fewer source documents
3. **Use gpt-4** for complex questions (slower but more accurate)
4. **Cache responses** for frequently asked questions

## Troubleshooting

### "OpenAI API Key not found"
```bash
# Make sure .env file exists with your API key
echo "OPENAI_API_KEY=sk-..." > .env
```

### "Vector store not found"
```bash
# Rebuild the vector store
python -c "from rag_chatbot import AIStartupRAG; rag = AIStartupRAG(); rag.build_vectorstore()"
```

### "No documents found in knowledge base"
1. Check that files exist in `knowledge_base/` directory
2. Supported formats: .md, .txt, .pdf
3. Ensure files are readable (not corrupted)
4. Call `/api/rebuild` endpoint after adding files

### Slow response times
1. Check your OpenAI API rate limits
2. Reduce the number of documents retrieved (change `k=3` in `_setup_qa_chain`)
3. Use `gpt-3.5-turbo` instead of `gpt-4`

### Port already in use
```bash
# Change the port
PORT=5001 python app.py
```

## Development

### Running Tests
```bash
# Coming soon: pytest suite
python -m pytest tests/
```

### Code Structure

**rag_chatbot.py**
- `AIStartupRAG` class - Main RAG system
- Document loading and processing
- Vector store management
- Query execution

**app.py**
- Flask application setup
- API endpoints
- Error handling
- CORS configuration

**templates/index.html**
- Web UI
- Real-time chat interface
- Source attribution display

### Extending the System

**Add new LLM models:**
```python
from langchain.chat_models import ChatAnthropic

self.llm = ChatAnthropic(model="claude-2")
```

**Use different vector stores:**
```python
from langchain.vectorstores import Pinecone

self.vectorstore = Pinecone.from_documents(docs, embeddings)
```

**Add custom retrieval:**
```python
self.retriever = self.vectorstore.as_retriever(
    search_kwargs={"k": 5, "filter": {"course": "AI101"}}
)
```

## Best Practices

1. **Organize your knowledge base** - Use subdirectories (raw, wiki, etc.)
2. **Include metadata** - Add source information to documents
3. **Regular updates** - Rebuild vector store after adding documents
4. **Monitor API usage** - Track OpenAI API costs
5. **Test thoroughly** - Verify answer quality with test questions
6. **Document sources** - Always attribute answers to documents

## Security Considerations

⚠️ **Important:**
- Keep your OpenAI API key secure (use environment variables)
- Don't commit `.env` files to version control
- Validate user input on the server side
- Rate limit API endpoints in production
- Use HTTPS in production
- Implement user authentication if needed

## License

This project is provided as-is for educational purposes.

## Support & Contribution

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review the code comments
3. Refer to LangChain documentation
4. Consult OpenAI API docs

---

**Built with ❤️ using LangChain, Flask, and OpenAI**

Last Updated: 2024-01-15
