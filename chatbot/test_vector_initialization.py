#!/usr/bin/env python3
"""
Test script to verify that vector store initialization works correctly when directories are deleted.
"""

import os
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def clean_vector_stores():
    """Remove existing vector store directories."""
    print("=== Cleaning Vector Stores ===")
    
    db_dir = os.getenv("CHROMA_DB_DIRECTORY", "./chroma_db")
    en_dir = f"{db_dir}_en"
    ja_dir = f"{db_dir}_ja"
    
    for directory in [en_dir, ja_dir]:
        if os.path.exists(directory):
            print(f"Removing directory: {directory}")
            shutil.rmtree(directory)
        else:
            print(f"Directory not found: {directory}")
    
    print("\nVector stores cleaned successfully.\n")
    return en_dir, ja_dir

def test_english_chatbot(en_dir):
    """Test English chatbot initialization with deleted directory."""
    print("=== Testing English Chatbot Initialization ===")
    
    print("Importing English chatbot...")
    from chatbot import GaussianFilterChatbot
    
    print("Creating English chatbot instance...")
    chatbot = GaussianFilterChatbot()
    print("English chatbot instance created.")
    
    if os.path.exists(en_dir):
        print(f"✓ English vector store directory created: {en_dir}")
        if os.path.exists(os.path.join(en_dir, "chroma.sqlite3")):
            print(f"✓ English vector store database file created")
            print("English chatbot test: PASSED\n")
        else:
            print(f"✗ English vector store database file not created")
            print("English chatbot test: FAILED\n")
    else:
        print(f"✗ English vector store directory not created: {en_dir}")
        print("English chatbot test: FAILED\n")

def test_japanese_chatbot(ja_dir):
    """Test Japanese chatbot initialization with deleted directory."""
    print("=== Testing Japanese Chatbot Initialization ===")
    
    print("Importing Japanese chatbot...")
    from ja_chatbot import GaussianFilterChatbotJa
    
    print("Creating Japanese chatbot instance...")
    chatbot = GaussianFilterChatbotJa()
    print("Japanese chatbot instance created.")
    
    if os.path.exists(ja_dir):
        print(f"✓ Japanese vector store directory created: {ja_dir}")
        if os.path.exists(os.path.join(ja_dir, "chroma.sqlite3")):
            print(f"✓ Japanese vector store database file created")
            print("Japanese chatbot test: PASSED\n")
        else:
            print(f"✗ Japanese vector store database file not created")
            print("Japanese chatbot test: FAILED\n")
    else:
        print(f"✗ Japanese vector store directory not created: {ja_dir}")
        print("Japanese chatbot test: FAILED\n")

def main():
    """Main test function."""
    print("=== Vector Store Initialization Test ===\n")
    
    if os.getenv("FORCE_REINDEX", "").lower() in ("true", "1", "yes"):
        print("Warning: FORCE_REINDEX is set to True in .env file.")
        print("This test may not accurately verify the fix.")
        print("Please set FORCE_REINDEX=False in .env file and run the test again.\n")
    
    en_dir, ja_dir = clean_vector_stores()
    
    test_english_chatbot(en_dir)
    
    test_japanese_chatbot(ja_dir)
    
    print("=== Test Summary ===")
    en_passed = os.path.exists(en_dir) and os.path.exists(os.path.join(en_dir, "chroma.sqlite3"))
    ja_passed = os.path.exists(ja_dir) and os.path.exists(os.path.join(ja_dir, "chroma.sqlite3"))
    
    if en_passed and ja_passed:
        print("✓ All tests passed!")
        print("The fix works correctly - vector stores are properly created when directories are deleted.")
    else:
        print("✗ Some tests failed.")
        print("The fix may not be working correctly - please check the log above for details.")

if __name__ == "__main__":
    main()
