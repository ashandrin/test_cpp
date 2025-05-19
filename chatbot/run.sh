#!/bin/bash


echo "===================================================="
echo "Gaussian Filter Chatbot / ガウスフィルターチャットボット"
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
