Overview
A chatbot that reads PDF files and answers questions related to their content. It splits the PDF into smaller
sections (chunks), generates embeddings for each chunk, and stores them in ChromaDB. When a user asks a
question, the chatbot retrieves the most relevant sections and uses the Gemini API to generate an answer based
on the retrieved context.
Tech Stack
Python: Main programming language.
PyMuPDF (fitz): Extracts text from PDF files.
Sentence Transformers (all-MiniLM-L6-v2): Converts text into embeddings.
ChromaDB: Stores and searches embeddings using a vector database.
Google Gemini API: Generates answers using the user's question and retrieved context.
Project Structure
ingest.py # Reads PDF files and stores embeddings in ChromaDB
ask.py # Answers questions using retrieved PDF content
requirements.txt # Contains the required Python libraries
Setup
1. Clone the repository and navigate to the project folder.
2. Create and activate a virtual environment:
py -3.12 -m venv venv
venv\Scripts\activate
3. Install the required libraries:
pip install -r requirements.txt
pip install google-genai python-dotenv
4. Create a .env file in the project folder and add your Gemini API key:
GEMINI_API_KEY=your_api_key_here
Important: Do not upload your .env file to GitHub. It should be included in .gitignore.
5. Add your PDF file to the project folder and rename it to sample.pdf.
Run the Project
First, process the PDF file:
python ingest.py
Then, start asking questions:
python ask.py
When the program displays Sawal:, enter your question. To exit the chatbot, type exit. RAG PDF Chatbot — Project Guide Page 2
Example
Question: What is Artificial Intelligence?
Answer: Artificial Intelligence (AI) is a branch of computer science that focuses on creating machines and systems
capable of performing tasks that typically require human intelligence.
Source pages: [1, 2]
Notes
• The embedding model is downloaded automatically the first time you run the project, so the initial setup may take
some time.
• The Gemini model name is defined in the MODEL variable inside ask.py.
• If the selected Gemini model is unavailable, replace it with another supported model.
Project Goal
To build an AI-powered PDF chatbot that understands document content, retrieves relevant information, and
provides context-based answers using Retrieval-Augmented Generation (RAG).