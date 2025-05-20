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
        
    def get_response_with_agent(self, user_input: str) -> str:
        """
        Get response using agent capabilities for questions not handled by RAG or pattern matching.
        Currently supports:
        - Counting lines of code in the repository
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string from the agent
        """
        if self._is_line_count_question(user_input):
            return self._count_code_lines()
            
        
        return None
        
    def _is_line_count_question(self, user_input: str) -> bool:
        """Check if the question is about code line count."""
        if self.language == "ja":
            return re.search(r'(行数|コード|ソース|ソフトウエア).*(数|教えて|カウント|数える)', user_input.lower()) is not None
        else:  # en
            if re.search(r'how many (line|code)', user_input.lower()) is not None:
                return True
            if re.search(r'(line|code).*(count|number)', user_input.lower()) is not None:
                return True
            if re.search(r'(count|tell me).*(line|code)', user_input.lower()) is not None:
                return True
            return False
            
    def _count_code_lines(self) -> str:
        """Count lines of code in the repository."""
        extensions = ['.cpp', '.h', 'Makefile']
        line_counts = {}
        total_lines = 0
        
        for extension in extensions:
            if extension == 'Makefile':
                makefile_path = Path(self.repo_path) / 'Makefile'
                if makefile_path.exists():
                    try:
                        with open(makefile_path, 'r') as f:
                            lines = len(f.readlines())
                            line_counts['Makefile'] = lines
                            total_lines += lines
                    except Exception as e:
                        print(f"Error counting lines in {makefile_path}: {e}")
                continue
                
            for file_path in Path(self.repo_path).glob(f"**/*{extension}"):
                if 'chatbot' in str(file_path):
                    continue
                    
                try:
                    with open(file_path, 'r') as f:
                        lines = len(f.readlines())
                        line_counts[str(file_path.relative_to(self.repo_path))] = lines
                        total_lines += lines
                except Exception as e:
                    print(f"Error counting lines in {file_path}: {e}")
        
        if self.language == "ja":
            response = f"ソフトウエアの合計行数は {total_lines} 行です。\n\n"
            response += "ファイル別の行数:\n"
        else:  # en
            response = f"The total number of lines of code in the software is {total_lines}.\n\n"
            response += "Lines of code by file:\n"
            
        for file, count in line_counts.items():
            response += f"- {file}: {count}\n"
            
        return response
        
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
            pattern_response = self.get_response_with_pattern_matching(user_input)
            
            if not pattern_response:
                agent_response = self.get_response_with_agent(user_input)
                if agent_response:
                    return agent_response
                return pattern_response
                
            return pattern_response
            
        return rag_response
        
    def show_greeting(self):
        """Display the initial greeting message (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
        
    def run(self):
        """Run the chatbot in interactive mode (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
