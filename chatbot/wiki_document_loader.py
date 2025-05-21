#!/usr/bin/env python3
"""
Utility for loading and processing Devin wiki software information.
"""

import os
from typing import List, Dict
from langchain.schema.document import Document
from document_loader import SourceCodeLoader

class WikiDocumentLoader(SourceCodeLoader):
    """Loader for Devin wiki software information."""
    
    def __init__(self, repo_path: str):
        """Initialize with the path to the repository."""
        super().__init__(repo_path)
        
    def load_wiki_info(self) -> List[Document]:
        """
        Load Devin wiki software information.
        
        Returns:
            List of documents with wiki information content
        """
        wiki_info = [
            {"title": "リポジトリの概要", "content": "プロジェクトの目的、主な機能、使用技術スタック、コード構造と依存関係"},
            {"title": "ディレクトリ構成", "content": "ファイル間の関係性、モジュールやクラスの依存関係"},
            {"title": "コアコンポーネントの解説", "content": "主要な関数・クラスの説明、処理フローやロジックの要点"},
            {"title": "アーキテクチャ図", "content": "コンポーネント間の関係性を視覚化、データフローや処理の流れを図示"},
            {"title": "APIドキュメント", "content": "関数やメソッドの引数・戻り値、使用例や内部動作の解説"},
            {"title": "デプロイメント情報", "content": "ビルド手順、実行・デプロイ方法"}
        ]
        
        documents = []
        for item in wiki_info:
            doc = Document(
                page_content=f"{item['title']}\n{item['content']}",
                metadata={"source": f"wiki_{item['title']}", "type": "wiki"}
            )
            documents.append(doc)
        
        return documents
