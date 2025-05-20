.PHONY: run setup help

run:
	python3 chatbot.py

setup:
	pip install -r requirements.txt
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it to add your OpenAI API key."; \
	fi

help:
	@echo "Gaussian Filter Chatbot (RAG-Enhanced)"
	@echo "----------------"
	@echo "make setup  - Install dependencies and create .env file"
	@echo "make run    - Run the chatbot in interactive mode"
	@echo "make help   - Show this help message"
