#!/usr/bin/env python3
"""
Vector database for storing and retrieving code embeddings.
"""

import os
from typing import List, Dict, Optional
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class VectorStore:
    """Vector store for code embeddings using ChromaDB."""
    
    def __init__(self, persist_directory: str, embedding_model: Optional[str] = None):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to store the vector database
            embedding_model: Name of the embedding model to use
        """
        self.persist_directory = persist_directory
        
        os.makedirs(persist_directory, exist_ok=True)
        
        if os.getenv("OPENAI_API_KEY") and embedding_model:
            self.embeddings = OpenAIEmbeddings(model=embedding_model)
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )
            
        self.db = None
        
    def index_documents(self, documents: List[Dict]) -> None:
        """
        Index documents in the vector store.
        
        Args:
            documents: List of documents to index
        """
        self.db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.db.persist()
        
    def load_existing_index(self) -> bool:
        """
        Load existing index if available.
        
        Returns:
            True if index was loaded successfully, False otherwise
        """
        if not os.path.exists(self.persist_directory):
            return False
            
        try:
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
            
    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search for similar documents in the vector store.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if not self.db:
            if not self.load_existing_index():
                raise ValueError("No index available. Please index documents first.")
                
        return self.db.similarity_search(query, k=k)
