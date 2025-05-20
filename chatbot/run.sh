#!/bin/bash

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "No .env file found. Creating from .env.example..."
        cp .env.example .env
        echo "Please edit the .env file to add your OpenAI API key for enhanced functionality."
        echo ""
    fi
fi

echo "===================================================="
echo "Gaussian Filter Chatbot (RAG-Enhanced) / ガウスフィルターチャットボット（RAG強化版）"
echo "===================================================="
echo "Please select your language / 言語を選択してください:"
echo "1. English"
echo "2. 日本語"
echo "===================================================="

read -p "Enter your choice (1/2): " choice

case $choice in
    1)
        python3 chatbot.py
        ;;
    2)
        python3 ja_chatbot.py
        ;;
    *)
        echo "Invalid choice. Defaulting to English."
        python3 chatbot.py
        ;;
esac
