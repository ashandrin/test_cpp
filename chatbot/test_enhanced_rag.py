#!/usr/bin/env python3
"""
Test script to verify enhanced RAG functionality with wiki information and reliability-based selection.
"""

import os
import sys
from dotenv import load_dotenv
from rag_chatbot import RAGChatbot

load_dotenv()

def test_wiki_info_inclusion():
    """Test if wiki information is included in the vector store."""
    print("=== Testing Wiki Information Inclusion ===")
    
    os.environ["FORCE_REINDEX"] = "True"
    chatbot = RAGChatbot()
    
    wiki_questions = [
        "リポジトリの概要について教えてください",
        "What is the architecture of the project?",
        "APIドキュメントはどこにありますか？",
        "Tell me about the deployment information"
    ]
    
    for question in wiki_questions:
        print(f"\nTesting question: {question}")
        response = chatbot.get_response_with_rag(question)
        
        if response:
            print(f"Response: {response[:150]}..." if len(response) > 150 else f"Response: {response}")
            print("✓ Response generated")
        else:
            print("✗ No response generated")
    
    print()

def test_reliability_selection():
    """Test reliability-based selection between RAG and agent responses."""
    print("=== Testing Reliability-Based Selection ===")
    
    chatbot = RAGChatbot()
    
    test_cases = [
        {
            "question": "How many lines of code are in the project?",
            "expected_winner": "agent"
        },
        {
            "question": "What is the Gaussian kernel algorithm?",
            "expected_winner": "rag"
        }
    ]
    
    for case in test_cases:
        question = case["question"]
        expected = case["expected_winner"]
        
        print(f"\nTesting question: {question}")
        print(f"Expected winner: {expected}")
        
        rag_response = chatbot.get_response_with_rag(question)
        agent_response = chatbot.get_response_with_agent(question)
        combined_response = chatbot.get_response(question)
        
        print(f"RAG response: {'Available' if rag_response else 'None'}")
        print(f"Agent response: {'Available' if agent_response else 'None'}")
        
        if rag_response and agent_response:
            rag_reliability = chatbot._calculate_response_reliability(question, rag_response, "rag")
            agent_reliability = chatbot._calculate_response_reliability(question, agent_response, "agent")
            
            print(f"RAG reliability: {rag_reliability:.2f}")
            print(f"Agent reliability: {agent_reliability:.2f}")
            
            actual_winner = "rag" if combined_response == rag_response else "agent"
            print(f"Actual winner: {actual_winner}")
            
            if actual_winner == expected:
                print("✓ Test passed")
            else:
                print("✗ Test failed")
        else:
            print("Cannot test reliability selection - missing responses")
    
    print()

def test_vector_prioritization():
    """Test prioritization of RAG answers for questions likely in vector store."""
    print("=== Testing Vector Store Prioritization ===")
    
    chatbot = RAGChatbot()
    
    vector_questions = [
        "Tell me about the code structure",
        "What files are in the repository?",
        "ソースコードの構成について説明してください"
    ]
    
    for question in vector_questions:
        print(f"\nTesting question: {question}")
        is_likely = chatbot._is_likely_in_vectorstore(question)
        print(f"Likely in vector store: {'Yes' if is_likely else 'No'}")
        
        if is_likely:
            print("✓ Question correctly identified as likely in vector store")
        else:
            print("✗ Question incorrectly identified as not in vector store")
    
    print()

def main():
    """Main test function."""
    print("=== Enhanced RAG Functionality Test ===\n")
    
    test_wiki_info_inclusion()
    test_reliability_selection()
    test_vector_prioritization()
    
    print("=== Test Summary ===")
    print("Wiki Information: Tested")
    print("Reliability Selection: Tested")
    print("Vector Prioritization: Tested")
    
    if not (os.getenv("OPENAI_API_KEY") or (os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"))):
        print("\nNote: No API keys detected. RAG responses were not generated.")
        print("To test RAG responses, set OPENAI_API_KEY or AZURE_OPENAI credentials in .env file.")

if __name__ == "__main__":
    main()
