#!/usr/bin/env python3
"""
Base class for RAG-enhanced Gaussian Filter chatbot.
"""

import os
import re
from typing import List, Dict, Optional, Union, Any
from dotenv import load_dotenv
from pathlib import Path

http_proxy = os.getenv("HTTP_PROXY")
if http_proxy:
    os.environ["HTTP_PROXY"] = http_proxy
https_proxy = os.getenv("HTTPS_PROXY")
if https_proxy:
    os.environ["HTTPS_PROXY"] = https_proxy
no_proxy = os.getenv("NO_PROXY")
if no_proxy:
    os.environ["NO_PROXY"] = no_proxy

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from vector_store import VectorStore
from document_loader import SourceCodeLoader
from knowledge_base import KNOWLEDGE_BASE, DETAILED_EXPLANATIONS

load_dotenv()

class RAGChatbot:
    """Base class for RAG-enhanced Gaussian Filter chatbot."""
    
    def __init__(self, repo_path: str = "../", language: str = "en", code_paths: Optional[List[str]] = None):
        """
        Initialize the RAG chatbot.
        
        Args:
            repo_path: Path to the repository
            language: Language for the chatbot (en or ja)
            code_paths: List of specific paths to analyze (optional)
        """
        self.repo_path = repo_path
        self.language = language
        self.code_paths = code_paths if code_paths else [repo_path]
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
        
        if self.vector_store.db:
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
            
            if self.vector_store.db:
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
        
        code_loader = SourceCodeLoader(self.repo_path, self.code_paths)
        code_documents = code_loader.load_source_files()
        
        try:
            from wiki_document_loader import WikiDocumentLoader
            wiki_loader = WikiDocumentLoader(self.repo_path)
            wiki_documents = wiki_loader.load_wiki_info()
            all_documents = code_documents + wiki_documents
            print(f"Loaded {len(code_documents)} code documents and {len(wiki_documents)} wiki documents")
        except ImportError:
            print("WikiDocumentLoader not found, proceeding with only code documents")
            all_documents = code_documents
        
        if not all_documents:
            print(f"Warning: No documents found in repository: {self.repo_path}")
            return
            
        chunks = code_loader.split_documents(all_documents)
        
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
            return ""
            
        try:
            result = self.chain.invoke({"question": user_input})
            return result["answer"]
        except Exception as e:
            print(f"Error getting response with RAG: {e}")
            return ""
    
    def get_response_with_pattern_matching(self, user_input: str) -> str:
        """
        Get response using pattern matching (to be implemented by subclasses).
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string from pattern matching
        """
        return ""
        
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
            
        
        return ""
        
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
        
    def _is_likely_in_vectorstore(self, user_input: str) -> bool:
        """
        Determine if a question is likely to be in the vector store.
        
        Args:
            user_input: User's input text
            
        Returns:
            True if question is likely to be in vector store, False otherwise
        """
        code_keywords = [
            'code', 'repository', 'function', 'class', 'method', 'implementation',
            'algorithm', 'structure', 'file', 'directory', 'module', 'コード', 'リポジトリ',
            '関数', 'クラス', 'メソッド', '実装', 'アルゴリズム', '構造', 'ファイル',
            'ディレクトリ', 'モジュール'
        ]
        
        for keyword in code_keywords:
            if keyword.lower() in user_input.lower():
                return True
                
        return False
        
    def _calculate_response_reliability(self, question: str, response: str, response_type: str) -> float:
        """
        Calculate the reliability of a response.
        
        Args:
            question: User's question
            response: Response text
            response_type: Type of response ('rag' or 'agent')
            
        Returns:
            Reliability score between 0 and 1
        """
        base_reliability = {
            "rag": 0.7,  # RAG is generally reliable for factual information
            "agent": 0.6  # Agent is slightly less reliable but good for computations
        }
        
        reliability = base_reliability.get(response_type, 0.5)
        
        if not response or len(response.strip()) < 10:
            return 0.1  # Very short responses are unreliable
            
        if response_type == "rag":
            if ('```' in response) or ('/' in response) or ('\\' in response):
                reliability += 0.2
                
            if any(char.isdigit() for char in response):
                reliability += 0.1
                
        elif response_type == "agent":
            if self._is_line_count_question(question):
                reliability += 0.3
                
            if any(char.isdigit() for char in response):
                reliability += 0.2
                
        return min(reliability, 1.0)
        
    def get_response(self, user_input: str) -> str:
        """
        Get response to user input.
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string
        """
        is_likely_in_vectorstore = self._is_likely_in_vectorstore(user_input)
        
        rag_response = self.get_response_with_rag(user_input)
        agent_response = self.get_response_with_agent(user_input)
        pattern_response = self.get_response_with_pattern_matching(user_input)
        
        if is_likely_in_vectorstore and rag_response:
            return rag_response
            
        if rag_response and agent_response:
            rag_reliability = self._calculate_response_reliability(user_input, rag_response, "rag")
            agent_reliability = self._calculate_response_reliability(user_input, agent_response, "agent")
            
            if rag_reliability > agent_reliability:
                return rag_response
            else:
                return agent_response
        
        if agent_response:
            return agent_response
        if rag_response:
            return rag_response
        return pattern_response
        
    def show_greeting(self):
        """Display the initial greeting message (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
        
    def run(self):
        """Run the chatbot in interactive mode (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")
