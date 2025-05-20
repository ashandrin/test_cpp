#!/usr/bin/env python3
"""
Base class for RAG-enhanced Gaussian Filter chatbot.
"""

import os
import re
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pathlib import Path

if os.getenv("HTTP_PROXY"):
    os.environ["HTTP_PROXY"] = os.getenv("HTTP_PROXY")
if os.getenv("HTTPS_PROXY"):
    os.environ["HTTPS_PROXY"] = os.getenv("HTTPS_PROXY")
if os.getenv("NO_PROXY"):
    os.environ["NO_PROXY"] = os.getenv("NO_PROXY")

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from vector_store import VectorStore
from document_loader import SourceCodeLoader
from knowledge_base import KNOWLEDGE_BASE, DETAILED_EXPLANATIONS

load_dotenv()

class RAGChatbot:
    """Base class for RAG-enhanced Gaussian Filter chatbot."""
    
    def __init__(self, repo_path: str = "../", language: str = "en"):
        """
        Initialize the RAG chatbot.
        
        Args:
            repo_path: Path to the repository
            language: Language for the chatbot (en or ja)
        """
        self.repo_path = repo_path
        self.language = language
        self.knowledge_base = KNOWLEDGE_BASE
        self.detailed_explanations = DETAILED_EXPLANATIONS
        self.greeting_shown = False
        
        db_dir = os.getenv("CHROMA_DB_DIRECTORY", "./chroma_db")
        self.vector_store = VectorStore(
            f"{db_dir}_{language}", 
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        )
        
        self.llm = None
        self.chain = None
        self.memory = None
        if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            self.setup_llm_azure()
        elif os.getenv("OPENAI_API_KEY"):
            self.setup_llm()
        
        self.initialize_vector_store()
        
    def setup_llm(self):
        """Set up the language model and conversation chain."""
        self.llm = ChatOpenAI(
            model_name=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
            temperature=0.5
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        if not self.vector_store.db:
            if not self.vector_store.load_existing_index():
                print("Warning: No vector index available. Running with limited capabilities.")
                return
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.db.as_retriever(),
            memory=self.memory
        )
        
    def setup_llm_azure(self):
        """Set up the Azure OpenAI language model and conversation chain."""
        try:
            self.llm = AzureChatOpenAI(
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "chat"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                temperature=0.5
            )
            
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            if not self.vector_store.db:
                if not self.vector_store.load_existing_index():
                    print("Warning: No vector index available. Running with limited capabilities.")
                    return
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.db.as_retriever(),
                memory=self.memory
            )
        except Exception as e:
            print(f"Error setting up Azure OpenAI: {e}")
            
    def initialize_vector_store(self):
        """Initialize the vector store with repository documents if not already done."""
        force_reindex = os.getenv("FORCE_REINDEX", "False").lower() in ("true", "1", "yes")
        
        if not force_reindex and self.vector_store.load_existing_index():
            print(f"Using existing vector index in {self.vector_store.persist_directory}")
            return
            
        print(f"Creating new vector index in {self.vector_store.persist_directory}")
        loader = SourceCodeLoader(self.repo_path)
        documents = loader.load_source_files()
        
        if not documents:
            print(f"Warning: No documents found in repository: {self.repo_path}")
            return
            
        chunks = loader.split_documents(documents)
        
        if not chunks:
            print("Warning: No document chunks created.")
            return
            
        print(f"Indexing {len(chunks)} document chunks...")
        self.vector_store.index_documents(chunks)
        print(f"Indexed {len(chunks)} document chunks in vector store: {self.vector_store.persist_directory}")
        
        if not self.llm:
            if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
                self.setup_llm_azure()
            elif os.getenv("OPENAI_API_KEY"):
                self.setup_llm()
    def get_response_with_rag(self, user_input: str) -> str:
        """
        Get response using RAG if available.
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string from the LLM
        """
        if not self.chain:
            return None
            
        try:
            result = self.chain.invoke({"question": user_input})
            return result["answer"]
        except Exception as e:
            print(f"Error getting response with RAG: {e}")
            return None
    
    def get_response_with_pattern_matching(self, user_input: str) -> str:
        """
        Get response using pattern matching (to be implemented by subclasses).
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string from pattern matching
        """
        raise NotImplementedError("Subclasses must implement this method.")
        
    def get_response(self, user_input: str) -> str:
        """
        Get response to user input.
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string
        """
        rag_response = self.get_response_with_rag(user_input)
        
        if not rag_response:
            return self.get_response_with_pattern_matching(user_input)
            
        return rag_response
        
    def show_greeting(self):
        """Display the initial greeting message (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
        
    def run(self):
        """Run the chatbot in interactive mode (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
