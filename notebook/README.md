# ShopGenie

ShopGenie is an end-to-end conversational product recommendation system built using Retrieval-Augmented Generation (RAG) on Flipkart product review data.

It helps users ask natural language shopping questions like:
- Which product has better bass quality?
- Best budget Bluetooth headset?
- Which item has better review sentiment overall?

The app retrieves relevant review context and generates concise responses through an LLM-powered chatbot.

## Project Highlights

- Complete RAG pipeline from raw CSV to final answer generation.
- Context-aware chatbot with conversational memory.
- Semantic retrieval using vector embeddings in Astra DB.
- Fast LLM response generation using Groq.
- Flask web interface for interactive Q and A.
- Dockerized application for portable deployment.
- AWS EC2 deployment-ready setup.
- CI/CD pipeline for automated deployment.

## Features

1. Product Recommendation Chatbot
- Users can ask product-related queries in simple language.
- The bot answers using retrieved review evidence.

2. Review-Aware Retrieval
- Retrieves top-k relevant chunks from product reviews.
- Improves response quality by grounding answers in data.

3. Conversation History Support
- Uses history-aware retrieval and message memory.
- Handles follow-up questions with context continuity.

4. Production-Oriented Packaging
- Works locally, in Docker, and on AWS EC2.

5. CI/CD Automation
- Automated build and deployment using GitHub Actions.
- Ensures consistent and fast delivery of updates.
 
## How The System Works

1. Data Ingestion
- Flipkart review CSV is read and prepared.

2. Data Conversion
- Each row is converted into LangChain Document format.
- Product title is stored as metadata.

3. Embedding + Vector Storage
- Review text embeddings are generated using Hugging Face inference API embeddings.
- Embeddings are stored in Astra DB vector collection.

4. Query Processing
- User question is reformulated (if needed) with chat history context.
- Relevant documents are retrieved from the vector store.

5. Answer Generation
- Retrieved context plus user question are sent to Groq LLM.
- Final concise answer is returned in chatbot UI.

## Complete Pipeline Implemented

This project includes the complete lifecycle:

1. Data pipeline
- CSV ingestion
- Document conversion
- Vector indexing

2. AI pipeline
- Retrieval
- Prompting
- Response generation
- Conversation memory

3. Application pipeline
- Flask backend routes
- HTML/CSS/JS chat frontend

4. Deployment pipeline
- Docker image build and run
- AWS EC2 hosting workflow

5. CI/CD pipeline
- Automated build, testing, and deployment using GitHub Actions

## Tech Stack

- Python 3.10
- Flask
- LangChain
- langchain-astradb
- langchain-groq
- langchain-community
- Hugging Face Inference API embeddings
- Astra DB (Vector Store)
- Docker
- AWS EC2
- GitHub Actions (CI/CD)

## Repository Structure

```text
.
|-- app.py
|-- requirements.txt
|-- setup.py
|-- Dockerfile
|-- aws.md
|-- data/
|   `-- flipkart_product_review.csv
|-- shopgenie/
|   |-- __init__.py
|   |-- data_converter.py
|   |-- data_ingestion.py
|   `-- retrieval_generation.py
|-- templates/
|   `-- index.html
|-- static/
|   `-- style.css
`-- notebook/
    `-- Flipkart_chatbot.ipynb
```

## Environment Variables

Create a .env file in project root:

```env
GROQ_API_KEY=your_groq_api_key
ASTRA_DB_API_ENDPOINT=your_astra_db_api_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_application_token
ASTRA_DB_KEYSPACE=your_astra_db_keyspace
HF_TOKEN=your_huggingface_token
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
python app.py
```

Open in browser:

```text
http://localhost:5000
```

## Docker Setup

Build image:

```bash
docker build -t shopgenie:latest .
```

Run container:

```bash
docker run -p 5000:5000 --env-file .env shopgenie:latest
```

## AWS EC2 Deployment Overview

1. Launch an EC2 instance.
2. Allow inbound traffic on app port (for example, 5000).
3. Install Docker on EC2.
4. Clone repository on EC2.
5. Build Docker image.
6. Run container with required environment variables.
7. Access app via EC2 public IP and configured port.

Detailed cloud steps are documented in aws.md.

## CI/CD Pipeline

Automated deployment is configured through the GitHub Actions workflow at .github/workflows/main.yaml.
The pipeline is responsible for build and deployment automation as part of the project delivery flow.

## API Endpoint

- GET / : serves chatbot web interface.
- POST /get : receives user message and returns generated answer.

## Data Source Note

The project uses a publicly available Flipkart review dataset. The CSV file name remains flipkart_product_review.csv to preserve source naming.

## Security Best Practices

- Never commit real API keys or tokens.
- Keep secrets only in .env or secret manager.
- Rotate any credential that was ever exposed.

## Future Improvements

- Add authentication and per-user session management.
- Improve retrieval quality with better chunking and metadata filters.
- Add evaluation metrics for response quality.
