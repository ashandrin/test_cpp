# Gaussian Filter Chatbot (RAG-Enhanced)

A chatbot that helps users understand the Gaussian filter implementation in the test_cpp repository, enhanced with RAG (Retrieval Augmented Generation) capabilities.

## Features

- Explains the code structure and functionality
- Provides information about Gaussian filtering concepts
- Answers questions about how to compile and run the application
- Gives detailed explanations of the algorithms used
- Uses RAG technology to provide more advanced responses based on source code analysis
- Supports both English and Japanese

## Requirements

- Python 3.6 or higher
- Dependencies listed in requirements.txt

## Installation

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Create a `.env` file from the template:

```
cp .env.example .env
```

3. Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

To run the chatbot:

```
./run.sh
```

Or directly:

```
python3 chatbot.py  # For English
python3 ja_chatbot.py  # For Japanese
```

## How It Works

The chatbot uses two approaches to answer questions:

1. **RAG (Retrieval Augmented Generation)**: When an OpenAI API key is provided, the chatbot:
   - Creates embeddings of the source code
   - Stores these embeddings in a vector database
   - Retrieves relevant code snippets based on the user's question
   - Generates a response using an LLM with the retrieved context

2. **Pattern Matching**: As a fallback or when no API key is provided, the chatbot:
   - Uses regular expressions to identify the topic of the question
   - Retrieves relevant information from a predefined knowledge base
   - Returns a structured response based on the identified topic

## Example Questions

- "What is this project about?"
- "Explain the code structure"
- "How does the Gaussian kernel function work?"
- "What is convolution?"
- "How do I compile and run the program?"
- "Explain the image processing pipeline"
- "What are the dependencies?"
- "Show me how the createGaussianKernel function works"
- "What does the main function do?"
