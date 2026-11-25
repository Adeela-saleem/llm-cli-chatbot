
# LLM CLI Chatbot

A command-line AI chatbot built using Python and Groq API.

## Features

- System prompt customization
- Streaming AI responses
- JSON output mode
- Input and output token tracking
- Per-message API cost calculation
- Conversation history
- Session usage tracking

## Technologies Used

- Python
- Groq API
- Groq Python SDK
- JSON
- python-dotenv

## Installation

1. Clone the repository:

   git clone YOUR_REPOSITORY_URL

2. Open the project folder:

   cd llm-cli-chatbot

3. Create virtual environment:

   python -m venv venv

4. Activate it (Windows):

   venv\Scripts\activate

5. Install dependencies:

   pip install groq python-dotenv

6. Create a .env file and add your API key:

   GROQ_API_KEY=your_api_key_here

7. Run the chatbot:

   python main.py

## Commands

- exit / quit / q : Exit chatbot
- /json : Toggle JSON output mode
