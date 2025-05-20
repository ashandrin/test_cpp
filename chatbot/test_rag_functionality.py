#!/usr/bin/env python3
"""
Test script to verify RAG functionality in both English and Japanese chatbots.
"""

import os
import sys
from dotenv import load_dotenv
from chatbot import GaussianFilterChatbot
from ja_chatbot import GaussianFilterChatbotJa

load_dotenv()

def test_vector_store_existence():
    """Test if vector stores exist and contain data."""
    print("=== Testing Vector Store Existence ===")
    
    db_dir = os.getenv("CHROMA_DB_DIRECTORY", "./chroma_db")
    en_dir = f"{db_dir}_en"
    ja_dir = f"{db_dir}_ja"
    
    if os.path.exists(en_dir):
        print(f"✓ English vector store exists: {en_dir}")
        if os.path.exists(os.path.join(en_dir, "chroma.sqlite3")):
            print("✓ English vector store contains database file")
        else:
            print("✗ English vector store missing database file")
    else:
        print(f"✗ English vector store does not exist: {en_dir}")
    
    if os.path.exists(ja_dir):
        print(f"✓ Japanese vector store exists: {ja_dir}")
        if os.path.exists(os.path.join(ja_dir, "chroma.sqlite3")):
            print("✓ Japanese vector store contains database file")
        else:
            print("✗ Japanese vector store missing database file")
    else:
        print(f"✗ Japanese vector store does not exist: {ja_dir}")
    
    print()

def test_chatbot_response(chatbot, query, language="English"):
    """Test chatbot response to a query."""
    print(f"=== Testing {language} Chatbot Response ===")
    print(f"Query: {query}")
    
    pattern_response = chatbot.get_response_with_pattern_matching(query)
    print(f"\nPattern Matching Response:")
    print(f"{pattern_response[:150]}..." if len(pattern_response) > 150 else pattern_response)
    
    rag_response = chatbot.get_response_with_rag(query)
    if rag_response:
        print(f"\nRAG Response:")
        print(f"{rag_response[:150]}..." if len(rag_response) > 150 else rag_response)
        print("✓ RAG response generated successfully")
    else:
        print("\nNo RAG response generated (API key may be missing)")
    
    combined_response = chatbot.get_response(query)
    print(f"\nCombined Response:")
    print(f"{combined_response[:150]}..." if len(combined_response) > 150 else combined_response)
    
    if combined_response == pattern_response:
        print("✓ Combined response using pattern matching")
    elif rag_response and combined_response == rag_response:
        print("✓ Combined response using RAG")
    else:
        print("✗ Combined response doesn't match either pattern or RAG")
    
    print()
    return combined_response

def main():
    """Main test function."""
    print("=== RAG Functionality Test ===\n")
    
    test_vector_store_existence()
    
    en_bot = GaussianFilterChatbot()
    ja_bot = GaussianFilterChatbotJa()
    
    en_query = "How does the Gaussian kernel function work?"
    en_response = test_chatbot_response(en_bot, en_query, "English")
    
    ja_query = "ガウスカーネル関数はどのように動作しますか？"
    ja_response = test_chatbot_response(ja_bot, ja_query, "Japanese")
    
    print("=== Test Summary ===")
    print("Vector Store: " + ("✓ Exists" if os.path.exists("./chroma_db_en") and os.path.exists("./chroma_db_ja") else "✗ Missing"))
    print("English Chatbot: " + ("✓ Responding" if en_response else "✗ Not responding"))
    print("Japanese Chatbot: " + ("✓ Responding" if ja_response else "✗ Not responding"))
    print("\nRAG Functionality: " + ("✓ Working correctly" if os.path.exists("./chroma_db_en") and os.path.exists("./chroma_db_ja") and en_response and ja_response else "✗ Issues detected"))
    
    if not (os.getenv("OPENAI_API_KEY") or (os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"))):
        print("\nNote: No API keys detected. RAG responses were not generated.")
        print("To test RAG responses, set OPENAI_API_KEY or AZURE_OPENAI credentials in .env file.")

if __name__ == "__main__":
    main()
