# Mini-Chatbot

A simple chat bot implementation using Ollama with the TinyLlama model. This project has no database or persistence—chat conversations reset when the page is refreshed.

## Setup and Installation

### Model Setup

To use the custom TinyLlama model:

1. Download and install Ollama locally
2. Run this command from the root of the repository:
   ```
   ollama create gunther -f model/Modelfile
   ```

### Docker Setup

Ensure Docker is running locally, then:

1. Pull the Ollama image:
   ```
   docker pull ollama/ollama
   ```

2. Run the container:
   ```
   docker run -d -v <Path to ollama dir>/.ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

### Backend Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install --ignore-installed -r requirements.txt
   ```

3. Start the FastAPI server:
   ```
   uvicorn backend.api.main:app --reload
   ```

### Frontend Setup

1. Make sure Node.js is installed
2. Navigate to the frontend directory:
   ```
   cd frontend
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## Usage

Access the chatbot through your web browser at the URL provided by the frontend development server (typically http://localhost:3000 or similar).