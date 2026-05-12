"""
AI Startup RAG Chatbot - Flask Web Application
Web interface and API for the RAG chatbot
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rag_chatbot import AIStartupRAG
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize RAG system
try:
    RAG_SYSTEM = AIStartupRAG(
        knowledge_dir=os.getenv("KNOWLEDGE_DIR", "./knowledge_base"),
        persist_dir=os.getenv("CHROMA_DB_DIR", "./chroma_db"),
        model_name=os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    )
    # Load or build vector store
    RAG_SYSTEM.load_vectorstore()
    logger.info("✅ RAG system initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize RAG system: {e}")
    RAG_SYSTEM = None


@app.route('/', methods=['GET'])
def index():
    """Serve the main chat interface"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "rag_initialized": RAG_SYSTEM is not None
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Expects: {"message": "user question"}
    Returns: {"answer": "...", "sources": [...]}
    """
    if RAG_SYSTEM is None:
        return jsonify({
            "error": "RAG system not initialized",
            "message": "Please check server logs"
        }), 500

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Query RAG system
        answer, source_documents = RAG_SYSTEM.query(user_message)

        # Format sources
        sources = []
        for doc in source_documents:
            sources.append({
                "title": doc.metadata.get('source', 'Unknown'),
                "excerpt": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })

        return jsonify({
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get RAG system statistics"""
    if RAG_SYSTEM is None:
        return jsonify({"error": "RAG system not initialized"}), 500

    try:
        stats = RAG_SYSTEM.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/rebuild', methods=['POST'])
def rebuild():
    """
    Rebuild the vector store from documents
    This should only be called after adding new documents to knowledge_base
    """
    if RAG_SYSTEM is None:
        return jsonify({"error": "RAG system not initialized"}), 500

    try:
        logger.info("Rebuilding RAG vector store...")
        RAG_SYSTEM.build_vectorstore()
        return jsonify({
            "status": "success",
            "message": "Vector store rebuilt successfully"
        }), 200
    except Exception as e:
        logger.error(f"Error rebuilding vector store: {e}")
        return jsonify({
            "error": "Failed to rebuild vector store",
            "message": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    logger.info(f"🚀 Starting AI Startup RAG Chatbot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
