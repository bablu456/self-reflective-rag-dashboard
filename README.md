# 🚀 Self-Reflective Agentic RAG Dashboard

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF4F00?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

> A production-grade SaaS dashboard featuring a LangGraph-powered AI Agent that grades its own retrieved context, rewrites search queries on failure, and visually exposes its reasoning process in real-time.

## The Problem vs. The Solution

### ❌ The Problem: "Naive" RAG
Standard Retrieval-Augmented Generation (RAG) pipelines blindly trust the documents they retrieve. They grab the top results and immediately generate an answer, regardless of whether those documents are actually relevant. This lack of validation is the leading cause of AI hallucinations when the search context is poor or ambiguous.

### ✅ The Solution: Agentic RAG
This project solves the hallucination problem by introducing a **LangGraph-driven state machine**. It acts like a meticulous human researcher:
1. **Retrieve:** Fetches context from the vector database.
2. **Grade:** Evaluates the retrieved context for strict relevance and sufficiency.
3. **Rewrite:** If the context fails the grading criteria, the agent dynamically *rewrites* the search query based on what it learned and searches again.
4. **Generate:** Produces a grounded answer *only* when it is confident the data is sufficient.

## Key Features

- **Split-Stack Architecture:** A robust decoupled design featuring a high-performance **FastAPI** backend and a modern **React (Next.js)** frontend.
- **React Flow Live Visualizer:** A stunning, node-based dynamic graph that pulses and lights up sequentially to show the AI's internal decision-making process in real-time.
- **Cross-Tab State Persistence:** Navigate seamlessly between Chat, Workflows, and Document management tabs without losing uploaded files or chat history (powered by React Context API).
- **Execution Latency Timer:** A built-in stopwatch badge provides precise, millisecond-accurate feedback on pipeline execution times.
- **Iteration Cap:** A hard limit of 3 retrieval loops prevents infinite loops on unanswerable questions, degrading gracefully to the best available context.

## Tech Stack

**Backend (Python):**
- **FastAPI:** High-performance REST API and server orchestration.
- **LangGraph & LangChain:** State machine orchestration for the retrieval-validation loop.
- **ChromaDB:** Local vector database for chunk storage and similarity search.
- **Google Gemini & Embeddings:** Powered by `gemma-4-26b-a4b-it` (LLM) and `gemini-embedding-001` for retrieval and evaluation.

**Frontend (TypeScript):**
- **React (Next.js):** Modern UI framework.
- **Tailwind CSS & shadcn/ui:** Modern, accessible, and sleek glassy dark-theme styling.
- **React Flow:** Interactive, node-based workflow visualization.

## How to Run Locally

> ⚠️ **STRICT NOTE:** Do not upload `.env` files to source control. You will need your own Google Gemini API key.

### 1. Clone the Repository
```bash
git clone https://github.com/Sumanth077/Hands-On-AI-Engineering.git
cd Hands-On-AI-Engineering/ai_agents/agentic_rag_system
```

### 2. Backend Setup
Navigate to the backend directory, set up your Python environment, and start the API server:

```bash
cd backend

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt  # Or use standard pip

# Set up environment variables
echo "GEMINI_API_KEY=your_google_ai_studio_key_here" > .env
```
*(Get your API key at [Google AI Studio](https://aistudio.google.com/app/apikey))*

Run the FastAPI server:
```bash
uvicorn main:app --reload
```
*The backend will now run at `http://localhost:8000`.*

### 3. Frontend Setup
Open a new terminal window, navigate to the frontend directory, and start the React application:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
# or npm start
```
*The frontend dashboard is now available at `http://localhost:3000`.*

## How It Works Under The Hood

```text
           ┌─────────────┐
           │   retrieve  │◄────────────────────┐
           └──────┬──────┘                     │
                  │                            │
           ┌──────▼──────────┐        ┌────────┴──────────┐
           │ grade_retrieval │──NO ──►│  rewrite_query    │
           └──────┬──────────┘        └───────────────────┘
                  │ YES (or max iterations reached)
           ┌──────▼──────┐
           │   generate  │
           └──────┬──────┘
                  │
                 END
```

## Author

**Bablu Kumar - Innovative AI Systems & Full Stack Engineer**  
Contributions, feedback, and pull requests are always welcome!
