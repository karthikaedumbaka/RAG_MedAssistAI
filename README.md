# Medical AI Assistant

A powerful RAG-based medical assistant that can answer questions based on uploaded medical PDFs.

![Medical AI Assistant](https://img.shields.io/badge/Medical-AI%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0+-red)

## 🌟 Features

- **PDF Document Processing**: Upload and process medical PDFs for information extraction
- **Natural Language Querying**: Ask questions about the medical documents in plain English
- **Source Citations**: Get answers with references to the source documents
- **Interactive UI**: User-friendly interface with loading animations and visual feedback
- **Sample PDFs**: Download sample medical PDFs directly from the application
- **Chat History**: Download your conversation history for future reference

## 🏗️ Architecture

The application follows a client-server architecture:

### Server (FastAPI)
- **PDF Processing**: Extracts text from uploaded PDFs
- **Vector Database**: Stores document embeddings for semantic search
- **LLM Integration**: Uses Google's Gemini model for generating responses
- **RAG Implementation**: Retrieval Augmented Generation for accurate answers

### Client (Streamlit)
- **User Interface**: Clean and intuitive interface for interacting with the assistant
- **File Upload**: Easy PDF upload functionality
- **Chat Interface**: Interactive chat with the AI assistant
- **Sample PDF Downloads**: Access to sample medical PDFs for testing

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- API keys for:
  - Google AI (Gemini)
  - Pinecone (Vector Database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Medical-AI-Assistant
   ```

2. Set up the server:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. Set up the client:
   ```bash
   cd ../client
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the server directory with the following variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_pinecone_index_name
   ```

### Running the Application

1. Start the server:
   ```bash
   cd ..
   python main.py
   ```

2. In a separate terminal, start the client:
   ```bash
   cd client
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## 📚 Usage

1. **Upload Medical PDFs**:
   - Click on the upload button in the sidebar
   - Select one or more PDF files
   - Wait for the processing to complete

2. **Download Sample PDFs**:
   - Use the "Sample PDFs for Testing" section in the sidebar
   - Click on the download links or the download button

3. **Ask Questions**:
   - Type your medical question in the chat input
   - Wait for the AI to process and respond
   - View the answer along with source citations

4. **Download Chat History**:
   - Click on the "Download Chat History" button
   - Save the conversation for future reference

## 🔧 Troubleshooting

- **API Key Issues**: Ensure all API keys are correctly set in the `.env` file
- **PDF Processing Errors**: Check that PDFs are not password-protected
- **Server Connection Issues**: Verify that the server is running on port 8000

## 🛠️ Technologies Used

- **FastAPI**: Backend API framework
- **Streamlit**: Frontend UI framework
- **LangChain**: Framework for LLM applications
- **Pinecone**: Vector database for document embeddings
- **Google Gemini**: Large Language Model for generating responses
- **PyPDF2**: PDF processing library


## 🙏 Acknowledgements

- Google AI for providing the Gemini API
- Pinecone for vector database services
- The open-source community for various libraries used in this project