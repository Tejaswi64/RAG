from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import ask_question
from retriever import search

app = FastAPI(
    title="RAG API",
    description="Retrieval-Augmented Generation API",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    n_results: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# endpoint
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Query endpoint for RAG.
    
    Args:
        question: The user's question
        n_results: Number of relevant chunks to retrieve (default: 3)
    
    Returns:
        answer: Generated answer from LLM
        sources: List of source chunks used
    """
    try:
        # Get answer from RAG
        answer = ask_question(request.question)
        
        # Get sources
        results = search(request.question, n_results=request.n_results)
        sources = results["documents"][0]
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)