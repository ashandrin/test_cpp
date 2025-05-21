#!/usr/bin/env python3
"""
Utility for loading and processing source code files from the repository.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class SourceCodeLoader:
    """Loads and processes source code files from the repository."""
    
    def __init__(self, repo_path: str, specific_paths: Optional[List[str]] = None):
        """
        Initialize with the path to the repository and optional specific paths.
        
        Args:
            repo_path: Base repository path
            specific_paths: List of specific paths to load (optional)
        """
        self.repo_path = Path(repo_path)
        self.specific_paths = specific_paths if specific_paths else [self.repo_path]
        
    def load_source_files(self, extensions: List[str] = ['.cpp', '.h', 'Makefile']) -> List[Dict]:
        """
        Load all source files with the specified extensions.
        
        Args:
            extensions: List of file extensions to include
            
        Returns:
            List of documents with source code content and metadata
        """
        documents = []
        
        for base_path in self.specific_paths:
            base_path = Path(base_path)
            
            for extension in extensions:
                if extension == 'Makefile':
                    makefile_path = base_path / 'Makefile'
                    if makefile_path.exists():
                        try:
                            loader = TextLoader(str(makefile_path))
                            documents.extend(loader.load())
                        except Exception as e:
                            print(f"Error loading {makefile_path}: {e}")
                    continue
                    
                for file_path in base_path.glob(f"**/*{extension}"):
                    if 'chatbot' in str(file_path):
                        continue
                        
                    try:
                        loader = TextLoader(str(file_path))
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
                    
        return documents
        
    def split_documents(self, documents: List[Dict], 
                        chunk_size: int = 1000, 
                        chunk_overlap: int = 200) -> List[Dict]:
        """
        Split documents into smaller chunks for better embedding.
        
        Args:
            documents: List of documents to split
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of document chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        return text_splitter.split_documents(documents)
