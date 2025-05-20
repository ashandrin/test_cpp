#!/usr/bin/env python3
"""
Script to force reindexing of vector store.
"""

import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def reindex_vector_store():
    """Force reindexing of vector store."""
    print("=== Reindexing Vector Store ===")
    
    os.environ["FORCE_REINDEX"] = "True"
    
    db_dir = os.getenv("CHROMA_DB_DIRECTORY", "./chroma_db")
    en_dir = f"{db_dir}_en"
    ja_dir = f"{db_dir}_ja"
    
    for directory in [en_dir, ja_dir]:
        if os.path.exists(directory):
            print(f"Removing existing directory: {directory}")
            shutil.rmtree(directory)
    
    print("\nCreating English vector store...")
    from chatbot import GaussianFilterChatbot
    en_bot = GaussianFilterChatbot()
    
    print("\nCreating Japanese vector store...")
    from ja_chatbot import GaussianFilterChatbotJa
    ja_bot = GaussianFilterChatbotJa()
    
    print("\nReindexing complete.")
    print(f"English vector store: {en_dir}")
    print(f"Japanese vector store: {ja_dir}")

if __name__ == "__main__":
    reindex_vector_store()
