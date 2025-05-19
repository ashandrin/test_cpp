# Gaussian Filter

A simple C++ application that applies a Gaussian blur filter to images using OpenCV.

## Features

- Applies an 8x8 Gaussian blur filter to input images
- Configurable input and output paths via command-line arguments
- Uses OpenCV for image processing operations

## Requirements

- C++ compiler with C++11 support
- OpenCV 4.x
- Make

## Building

```
make
```

## Usage

```
./gaussian_filter [input_path] [output_path]
```

Where:
- `input_path` is the path to the input image (optional, defaults to a hardcoded path)
- `output_path` is the path for the output image (optional, defaults to `output.jpg` in the current directory)

## Chatbot

An AI-powered chatbot is available to help understand this codebase. To use the chatbot:

```
cd chatbot
./run.sh
```

The chatbot can answer questions about:
- The project structure and files
- How the Gaussian filter works
- The code implementation details
- How to compile and use the software
- Specific concepts like kernels, convolution, etc.

The chatbot is available in both English and Japanese and uses RAG (Retrieval Augmented Generation) technology to provide detailed explanations based on the source code.

For full functionality, an OpenAI API key is required. See the chatbot README for setup instructions.
