from fastapi import FastAPI
from pydantic import BaseModel
from graph import run_assistant
from schemas import SupportResponse

app = FastAPI(
    title="Zepto Support Assistant"
)

class AskRequest(BaseModel):
    query: str

@app.post("/ask", response_model=SupportResponse)
def ask(request: AskRequest):
    """Process a customer question."""
    result = run_assistant(request.query)
    return SupportResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )