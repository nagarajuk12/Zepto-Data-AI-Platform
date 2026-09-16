import os
from typing import TypedDict
import chromadb
from langgraph.graph import StateGraph, START, END
from sentence_transformers import SentenceTransformer
from prompt import build_prompt
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configurations
CHROMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)

COLLECTION_NAME = "zepto_support"
MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_MODEL = "groq/compound-mini"

# MOCK_LLM unset or "1" for Mock mode
# MOCK_LLM="0" = optional -> real LLM mode
MOCK_LLM = os.getenv("MOCK_LLM", "1")

# Define LangGraph State
class SupportState(TypedDict):
    query: str
    intent: str
    context: list[str]
    sources: list[str]
    answer: str
    confidence: float

# Load embedding model and ChromaDB
embedding_model = SentenceTransformer(MODEL_NAME)
chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)
collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)

# Create Realtime LLM Client API call
def create_llm_client():
    """Create the Groq LLM client and handle configuration errors."""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        print(api_key)

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. "
                "Please set the GROQ_API_KEY environment variable."
            )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. "
                "Please set the GROQ_API_KEY environment variable."
            )
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=GROQ_MODEL,
            temperature=0
        )
    except Exception as error:
        print(f"Failed to create Groq LLM client: {error}")
        return None

# Node 1: Classify Intent
def classify_intent(state):
    """
    Classify the query as policy_question or general_question.
    Mock mode uses the required keyword heuristic.
    Real mode optionally uses an LLM.
    """
    query = state["query"]
    lower_query = query.lower()
    keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]
    # Required to be graded baseline
    if MOCK_LLM != "0":
        if any(keyword in lower_query for keyword in keywords):
            intent = "policy_question"
        else:
            intent = "general_question"

    # Optional real LLM path
    else:
        llm = create_llm_client()
        prompt = f"""
Classify the following customer query as exactly one of:

policy_question
general_question

Use policy_question when the query asks about a Zepto policy.
Use general_question when it does not.

Customer query:
{query}

Return only one classification.
"""
        response = llm.invoke(prompt)
        intent = response.content.strip()
        if intent not in {
            "policy_question",
            "general_question"
        }:
            intent = "general_question"

    return {
        "intent": intent
    }

# Node 2: Retrieve and Answer
def retrieve_and_answer(state):
    """
    Retrieve the top 3 similar policy chunks and generate an answer.
    Retrieval always happens locally.
    """
    query = state["query"]
    # Generate query embedding locally
    query_embedding = embedding_model.encode(
        query
    ).tolist()
    # Retrieve top 3 chunks from ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    context = documents
    sources = [
        metadata["source"]
        for metadata in metadatas
        if "source" in metadata
    ]
    # Required mock mode
    if MOCK_LLM != "0":
        top_chunk_snippet = documents[0][:200]
        answer = (
            f"Based on the retrieved context: "
            f"{top_chunk_snippet}"
        )
        confidence = 1.0
    else:
        # Optional real LLM mode
        context_text = "\n\n".join(
            documents
        )
        prompt = build_prompt(
            context=context_text,
            question=query
        )
        llm = create_llm_client()
        response = llm.invoke(prompt)
        answer = response.content
        confidence = 1.0

    return {
        "context": context,
        "sources": sources,
        "answer": answer,
        "confidence": confidence
    }


# Node 3: Direct Answer
def direct_answer(state):
    """
    Answer general questions without retrieval.
    """
    query = state["query"]

    # Required mock mode
    if MOCK_LLM != "0":
        answer = (
            "I can only answer questions about Zepto policies right now."
        )
        confidence = 1.0
    # Optional real LLM mode
    else:
        prompt = f"""
You are Zepto's customer support assistant.
Answer the following customer question directly.
Customer question:
{query}
Keep the answer concise and helpful.
"""
        llm = create_llm_client()
        response = llm.invoke(prompt)
        answer = response.content
        confidence = 1.0
    return {
        "answer": answer,
        "sources": [],
        "confidence": confidence
    }

# Conditional Router
def route_intent(state):
    """
    Route the graph based on the classified intent.
    """
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"
    return "direct_answer"

# Build LangGraph
def build_graph():
    """Build and compile the LangGraph workflow."""
    graph = StateGraph(SupportState)
    # Add required nodes
    graph.add_node(
        "classify_intent",
        classify_intent
    )
    graph.add_node(
        "retrieve_and_answer",
        retrieve_and_answer
    )
    graph.add_node(
        "direct_answer",
        direct_answer
    )
    # Start → classify
    graph.add_edge(
        START,
        "classify_intent"
    )
    # Conditional routing
    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer"
        }
    )
    # Both paths → END
    graph.add_edge(
        "retrieve_and_answer",
        END
    )
    graph.add_edge(
        "direct_answer",
        END
    )
    return graph.compile()

# Run Assistant
def run_assistant(query: str):
    """Run a customer query through the LangGraph."""
    graph = build_graph()
    initial_state: SupportState = {
        "query": query
    }
    return graph.invoke(initial_state)

# Validation / Testing
if __name__ == "__main__":
    result = run_assistant(
        #"How long does Zepto delivery take?"
        #"who is CEO of  Zepto"
        #"When will I receive my refund?"
        "How much does Zepto Pass cost?"
    )
    print("\nIntent:")
    print(result["intent"])
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    print(result["sources"])
    print("\nConfidence:")
    print(result["confidence"])