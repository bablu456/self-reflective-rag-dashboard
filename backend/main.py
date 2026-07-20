import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import tempfile

# pyrefly: ignore [missing-import]
from rag_graph import app as rag_app, embeddings, CHROMA_DB_PATH

# ── FastAPI Setup ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Self-Reflective Agentic RAG API",
    description="Backend API for the Self-Reflective Agentic RAG system.",
    version="1.0.0",
)

# Allow React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    iterations: int
    reflection_log: List[str]

# ── API Endpoints ──────────────────────────────────────────────────────────────


@app.get("/")
def helath_check():
    return {"Status": "Healthy","Message": "Agentic RAG API is running."}
    

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint for uploading a PDF document.
    Saves it to a temporary file, processes it, and persists to ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Clear existing DB
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)

        # Write uploaded file to a temporary file to use with PyPDFLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(tmp_file_path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DB_PATH)
        finally:
            os.remove(tmp_file_path) # Clean up temp file

        return {
            "status": "success",
            "message": f"Successfully indexed {len(chunks)} chunks from {len(docs)} pages."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: QueryRequest):
    """
    Endpoint to ask a question.
    Invokes the LangGraph RAG pipeline and returns the final generated answer along with the reflection history.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if not os.path.exists(CHROMA_DB_PATH):
        raise HTTPException(status_code=400, detail="No document loaded. Upload a PDF first.")

    try:
        result = rag_app.invoke({
            "question": request.question.strip(),
            "refined_query": "",
            "context": "",
            "reflection": "",
            "answer": "",
            "iterations": 0,
            "reflection_log": [],
        })

        reflection_log = result.get("reflection_log", [])
        iterations = result.get("iterations", 0)
        answer = result.get("answer", "No answer was generated.")

        return ChatResponse(
            answer=answer,
            iterations=iterations,
            reflection_log=reflection_log
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during inference: {str(e)}")

@app.delete("/api/clear")
async def clear_database():
    """
    Safely deletes the ChromaDB persistent directory to reset the system.
    """
    try:
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)
            return {"status": "success", "message": "Database cleared successfully."}
        else:
            return {"status": "success", "message": "Database was already empty."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")
