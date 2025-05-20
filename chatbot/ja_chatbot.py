#!/usr/bin/env python3
"""
test_cppリポジトリのガウスフィルター実装を説明するチャットボット。
RAG機能を使用して高度な応答を生成します。
"""

import re
import sys
import os
from dotenv import load_dotenv
from ja_knowledge_base import JA_KNOWLEDGE_BASE, JA_DETAILED_EXPLANATIONS
from rag_chatbot import RAGChatbot

load_dotenv()

class GaussianFilterChatbotJa(RAGChatbot):
    def __init__(self, repo_path: str = "../"):
        """指定されたリポジトリパスでチャットボットを初期化します。"""
        super().__init__(repo_path=repo_path, language="ja")
        self.knowledge_base = JA_KNOWLEDGE_BASE
        self.detailed_explanations = JA_DETAILED_EXPLANATIONS
        
    def show_greeting(self):
        """初期挨拶メッセージを表示します。"""
        print("="*80)
        print("ガウスフィルターチャットボット（RAG強化版）")
        print("="*80)
        print("ようこそ！test_cppリポジトリのガウスフィルター実装について理解するお手伝いをします。")
        print("以下について質問できます：")
        print("- プロジェクト構造とファイル")
        print("- ガウスフィルターの仕組み")
        print("- コード実装の詳細")
        print("- ソフトウェアのコンパイルと使用方法")
        print("- カーネル、畳み込みなどの特定の概念")
        print("\n会話を終了するには「終了」、「quit」、または「bye」と入力してください。")
        print("このメッセージをもう一度表示するには「ヘルプ」と入力してください。")
        
        if (os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT") and self.llm):
            print("\n[Azure OpenAIを使用したAI応答機能が有効です]")
        elif os.getenv("OPENAI_API_KEY") and self.llm:
            print("\n[OpenAIを使用したAI応答機能が有効です]")
        else:
            print("\n[基本モードで実行中 - AI応答機能を有効にするにはOPENAI_API_KEYまたはAZURE_OPENAI_API_KEYを設定してください]")
            
        print("="*80)
        self.greeting_shown = True
    
    def get_response_with_pattern_matching(self, user_input):
        """パターンマッチングを使用してユーザー入力を処理し、応答を生成します。"""
        user_input = user_input.lower().strip()
        
        if user_input in ['終了', 'quit', 'bye', 'exit']:
            return "さようなら！ガウスフィルター実装の理解にお役に立てれば幸いです。"
        
        if user_input in ['ヘルプ', 'help', '?']:
            self.show_greeting()
            return ""
        
        if re.search(r'何|なに|について|目的|プロジェクト|リポジトリ|何ですか', user_input):
            return self._get_project_info()
        
        if re.search(r'コード|構造|ファイル|組織|構成', user_input):
            return self._get_code_structure()
        
        if re.search(r'カーネル|関数|creategaussiankernel|作成|ガウス関数', user_input):
            return self._get_kernel_function_info()
        
        if re.search(r'メイン|main|エントリー|プログラムフロー|実行', user_input):
            return self._get_main_function_info()
        
        if re.search(r'概念|ガウス|ぼかし|シグマ|畳み込み|フィルター|正規化', user_input):
            return self._get_concept_info(user_input)
        
        if re.search(r'使用|使い方|方法|実行|コンパイル|ビルド|コマンド|引数', user_input):
            return self._get_usage_info()
        
        if re.search(r'依存|opencv|ライブラリ|要件', user_input):
            return self._get_dependency_info()
        
        if re.search(r'アルゴリズム|詳細|説明|どのように|パイプライン|処理', user_input):
            if 'カーネル' in user_input or 'ガウス' in user_input:
                return self.detailed_explanations['gaussian_kernel_algorithm']
            if 'パイプライン' in user_input or '処理' in user_input or '画像' in user_input:
                return self.detailed_explanations['image_processing_pipeline']
        
        return ("その質問にどう答えるべきかわかりません。プロジェクト、コード構造、"
                "ガウスカーネル関数、メイン関数、概念、使用方法、または依存関係について"
                "質問できます。詳細については「ヘルプ」と入力してください。")
                
    def get_response(self, user_input):
        """ユーザー入力に対する応答を取得し、可能であればRAGを使用します。"""
        user_input = user_input.lower().strip()
        
        if user_input in ['終了', 'quit', 'bye', 'exit']:
            return "さようなら！ガウスフィルター実装の理解にお役に立てれば幸いです。"
        
        if user_input in ['ヘルプ', 'help', '?']:
            self.show_greeting()
            return ""
        
        agent_response = self.get_response_with_agent(user_input)
        if agent_response:
            return agent_response
            
        rag_response = self.get_response_with_rag(user_input)
        if not rag_response:
            return self.get_response_with_pattern_matching(user_input)
            
        return rag_response
    
    def _get_project_info(self):
        """プロジェクトに関する情報を取得します。"""
        project = self.knowledge_base['project']
        return (f"プロジェクト: {project['name']}\n\n"
                f"説明: {project['description']}\n\n"
                f"リポジトリ: {project['repository']}\n\n"
                f"主要ファイル: {', '.join(project['files'])}")
    
    def _get_code_structure(self):
        """コード構造に関する情報を取得します。"""
        structure = self.knowledge_base['code_structure']
        result = "コード構造:\n\n"
        for file, description in structure.items():
            result += f"• {file}: {description}\n"
        return result
    
    def _get_kernel_function_info(self):
        """ガウスカーネル関数に関する情報を取得します。"""
        func = self.knowledge_base['functions']['createGaussianKernel']
        
        result = f"関数: createGaussianKernel\n\n"
        result += f"目的: {func['purpose']}\n\n"
        
        result += "パラメータ:\n"
        for param in func['parameters']:
            result += f"• {param['name']} ({param['type']}): {param['description']}\n"
        
        result += f"\n戻り値: {func['return']['type']} - {func['return']['description']}\n\n"
        result += f"アルゴリズム: {func['algorithm']}\n\n"
        result += f"詳細については、「ガウスカーネルアルゴリズム」について質問してください。"
        
        return result
    
    def _get_main_function_info(self):
        """メイン関数に関する情報を取得します。"""
        func = self.knowledge_base['functions']['main']
        
        result = f"関数: main\n\n"
        result += f"目的: {func['purpose']}\n\n"
        
        result += "パラメータ:\n"
        for param in func['parameters']:
            result += f"• {param['name']} ({param['type']}): {param['description']}\n"
        
        result += f"\n戻り値: {func['return']['type']} - {func['return']['description']}\n\n"
        result += f"アルゴリズム: {func['algorithm']}\n\n"
        result += f"詳細については、「画像処理パイプライン」について質問してください。"
        
        return result
    
    def _get_concept_info(self, user_input):
        """概念に関する情報を取得します。"""
        concepts = self.knowledge_base['concepts']
        
        for concept, description in concepts.items():
            if concept.replace('_', ' ') in user_input:
                return f"{concept.replace('_', ' ')}: {description}"
        
        result = "ガウス画像フィルタリングの概念:\n\n"
        for concept, description in concepts.items():
            result += f"• {concept.replace('_', ' ')}: {description}\n\n"
        
        return result
    
    def _get_usage_info(self):
        """使用方法に関する情報を取得します。"""
        usage = self.knowledge_base['usage']
        
        result = "ガウスフィルターの使用方法:\n\n"
        result += f"コンパイル: {usage['compilation']}\n\n"
        result += f"実行: {usage['execution']}\n\n"
        
        result += "コマンドライン引数:\n"
        for arg in usage['command_line_args']:
            result += f"• {arg['name']}: {arg['description']}\n"
        
        result += "\n例:\n"
        for example in usage['examples']:
            result += f"• {example['command']}\n  {example['description']}\n"
        
        return result
    
    def _get_dependency_info(self):
        """依存関係に関する情報を取得します。"""
        deps = self.knowledge_base['dependencies']
        
        result = "依存関係:\n\n"
        for _, dep in deps.items():
            result += f"{dep['name']}: {dep['description']}\n"
            result += f"バージョン: {dep['version']}\n\n"
            
            result += "使用されるコンポーネント:\n"
            for comp in dep['components_used']:
                result += f"• {comp['name']}: {comp['purpose']}\n"
        
        return result
    
    def run(self):
        """チャットボットをインタラクティブモードで実行します。"""
        self.show_greeting()
        
        try:
            while True:
                user_input = input("\nあなた: ").strip()
                if not user_input:
                    continue
                
                response = self.get_response(user_input)
                if response:
                    print(f"\nチャットボット: {response}")
                
                if user_input.lower() in ['終了', 'quit', 'bye', 'exit']:
                    break
        except KeyboardInterrupt:
            print("\n\nさようなら！ガウスフィルター実装の理解にお役に立てれば幸いです。")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    chatbot = GaussianFilterChatbotJa()
    chatbot.run()
