"""
AI Startup RAG Chatbot - Core RAG System
Main module for handling document processing and RAG queries
"""

import os
import json
from pathlib import Path
from typing import List, Tuple
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class AIStartupRAG:
    """
    RAG system for AI Startup course materials
    Supports: RAW files, Wiki documentation, Master index
    """

    def __init__(self,
                 knowledge_dir: str = "./knowledge_base",
                 persist_dir: str = "./chroma_db",
                 model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the RAG system

        Args:
            knowledge_dir: Directory containing course materials
            persist_dir: Directory to persist vector database
            model_name: LLM model to use
        """
        self.knowledge_dir = knowledge_dir
        self.persist_dir = persist_dir
        self.model_name = model_name

        # Initialize embeddings and LLM
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=1024
        )

        # Initialize vector store (will be populated by load_documents)
        self.vectorstore = None
        self.qa_chain = None

        # Create knowledge directory if it doesn't exist
        Path(knowledge_dir).mkdir(parents=True, exist_ok=True)

    def load_documents(self) -> List:
        """
        Load documents from the knowledge base directory
        Supports: .md, .txt, .pdf files
        """
        documents = []

        # Load markdown files
        if Path(self.knowledge_dir).exists():
            # Load all text files
            loader = DirectoryLoader(
                self.knowledge_dir,
                glob="**/*.md",
                loader_cls=TextLoader
            )
            try:
                documents.extend(loader.load())
            except:
                pass

            # Load txt files
            loader = DirectoryLoader(
                self.knowledge_dir,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            try:
                documents.extend(loader.load())
            except:
                pass

        if not documents:
            print("⚠️  No documents found in knowledge base. Using sample data...")
            documents = self._create_sample_documents()

        print(f"✅ Loaded {len(documents)} documents")
        return documents

    def _create_sample_documents(self) -> List:
        """Create sample documents for demo purposes"""
        from langchain.schema import Document

        sample_content = [
            {
                "title": "AI Startup Fundamentals",
                "content": """
                # AI Startup Fundamentals

                ## What is an AI Startup?
                An AI startup is a company that uses artificial intelligence as its core technology
                to solve business problems or create new products.

                ## Key Characteristics
                1. Heavy focus on ML/AI technology
                2. Data-driven decision making
                3. Fast iteration cycles
                4. Scalable solutions

                ## Common Challenges
                - Finding quality training data
                - Talent acquisition
                - Balancing innovation with business metrics
                """
            },
            {
                "title": "Machine Learning Basics",
                "content": """
                # Machine Learning for Startups

                ## Types of ML
                1. Supervised Learning - labeled data
                2. Unsupervised Learning - finding patterns
                3. Reinforcement Learning - learning through interaction

                ## Important Considerations
                - Data quality > quantity
                - Model interpretability
                - Ethical implications
                - Regulatory compliance
                """
            },
            {
                "title": "Building AI Products",
                "content": """
                # Building Successful AI Products

                ## MVP Strategy
                1. Define clear problem
                2. Gather minimum viable data
                3. Build simple baseline model
                4. Get user feedback
                5. Iterate

                ## Metrics That Matter
                - Accuracy for classification tasks
                - Latency/response time
                - User satisfaction
                - Cost efficiency
                """
            }
        ]

        documents = []
        for doc in sample_content:
            documents.append(Document(
                page_content=doc["content"],
                metadata={"source": doc["title"]}
            ))

        return documents

    def build_vectorstore(self, documents: List = None):
        """
        Build or rebuild the vector store with documents
        """
        if documents is None:
            documents = self.load_documents()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} document chunks")

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir,
            collection_name="ai_startup"
        )

        self._setup_qa_chain()
        print(f"✅ Vector store created and saved to {self.persist_dir}")

    def load_vectorstore(self):
        """Load existing vector store from disk"""
        if not Path(self.persist_dir).exists():
            print("⚠️  Vector store not found. Building new one...")
            self.build_vectorstore()
        else:
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
                collection_name="ai_startup"
            )
            self._setup_qa_chain()
            print("✅ Vector store loaded from disk")

    def _setup_qa_chain(self):
        """Setup the QA chain with custom prompt"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call load_vectorstore() first.")

        # Custom prompt template
        prompt_template = """Use the following pieces of context to answer the question.
If you don't know the answer from the context, say so clearly.

Context:
{context}

Question: {question}

Answer: """

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Return top 3 relevant documents
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

    def query(self, question: str) -> Tuple[str, List]:
        """
        Query the RAG system

        Args:
            question: User's question

        Returns:
            Tuple of (answer, source_documents)
        """
        if self.qa_chain is None:
            raise ValueError("QA chain not initialized. Call load_vectorstore() first.")

        result = self.qa_chain({"query": question})

        return result["result"], result.get("source_documents", [])

    def get_stats(self) -> dict:
        """Get statistics about the RAG system"""
        if self.vectorstore is None:
            return {"status": "Not initialized"}

        return {
            "model": self.model_name,
            "vector_store": self.persist_dir,
            "embedding_model": "OpenAI",
            "status": "Ready"
        }


def main():
    """Demo usage of the RAG system"""
    # Initialize RAG
    rag = AIStartupRAG()

    # Build vector store
    print("Building RAG system...")
    rag.build_vectorstore()

    # Example queries
    test_questions = [
        "What are the key characteristics of an AI startup?",
        "Tell me about machine learning basics",
        "How should I build an AI product?"
    ]

    print("\n" + "="*50)
    print("Testing RAG Chatbot")
    print("="*50)

    for question in test_questions:
        print(f"\n❓ Question: {question}")
        answer, sources = rag.query(question)
        print(f"✅ Answer: {answer}")
        if sources:
            print(f"📚 Sources:")
            for doc in sources:
                print(f"   - {doc.metadata.get('source', 'Unknown')}")


if __name__ == "__main__":
    main()
