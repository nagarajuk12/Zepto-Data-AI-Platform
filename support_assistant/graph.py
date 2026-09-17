import os
import json
from typing import TypedDict
import chromadb
from langgraph.graph import StateGraph, START, END
from sentence_transformers import SentenceTransformer
from prompt import build_prompt
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from schemas import SupportResponse

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
# MOCK_LLM="0" = optional -> Real LLM mode
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

def generate_valid_response(llm, prompt):
    """    Generate a structured LLM response.
    First attempt + up to 2 additional retries.
    """
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = llm.invoke(prompt)
            raw_output = response.content
            parsed_output = json.loads(raw_output)
            validated_response = SupportResponse.model_validate(
                parsed_output
            )

            return validated_response

        except Exception as error:
            print(
                f"Validation failed "
                f"(attempt {attempt + 1}/{max_attempts}): {error}"
            )

            # Two additional attempts are allowed
            if attempt < 2:
                prompt = f"""
                Your previous response failed validation.
                
                Validation error:
                {error}
                
                Return ONLY valid JSON matching this schema:
                
                {{
                    "answer": "string",
                    "sources": ["string"],
                    "confidence": 0.0
                }}
                
                Requirements:
                - answer must be a string
                - sources must be a list of strings
                - confidence must be between 0 and 1
                - do not include Markdown
                - do not include code fences
                - do not include any text outside the JSON object
                
                Original request:
                {prompt}
                """

    return SupportResponse(
        answer=(
            "ERROR: Unable to generate a valid structured "
            "response after 3 attempts."
        ),
        sources=[],
        confidence=0.0
    )

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
        metadata["chunk_id"]
        for metadata in metadatas
        if "chunk_id" in metadata
    ]
    # Required mock mode
    if MOCK_LLM != "0":
        top_chunk_snippet = documents[0][:200]
        response = SupportResponse(
            answer=(
                f"Based on the retrieved context: "
                f"{top_chunk_snippet}"
            ),
            sources=sources,
            confidence=1.0
        )
    else:
        # Optional real LLM mode
        context_text = "\n\n".join(documents)
        prompt = build_prompt(
            context=context_text,
            question=query
        )
        llm = create_llm_client()
        if llm is None:
            return {
                "context": context,
                "sources": [],
                "answer": "ERROR: LLM client could not be initialized.",
                "confidence": 0.0
            }
        response = generate_valid_response(
            llm,
            prompt
        )

    return {
        "context": context,
        "sources": response.sources,
        "answer": response.answer,
        "confidence": response.confidence
    }

# Node 3: Direct Answer
def direct_answer(state):
    """
    Answer general questions without retrieval.
    """
    query = state["query"]

    # Required mock mode
    if MOCK_LLM != "0":
        response = SupportResponse(
                answer=(
                    "I can only answer questions about "
                    "Zepto policies right now."
                ),
                sources=[],
                confidence=1.0
            )
    # Optional real LLM mode
    else:
        prompt = f"""
        You are Zepto's customer support assistant.
        Answer the following customer question directly.
        Customer question:
        {query}
        Return ONLY valid JSON:
        
        {{
            "answer": "string",
            "sources": [],
            "confidence": 0.0
        }}
        
        The sources list must be empty.
        Confidence must be between 0 and 1.
        """
        llm = create_llm_client()
        if llm is None:
            return {
                "answer": "ERROR: LLM client could not be initialized.",
                "sources": [],
                "confidence": 0.0
            }

        response = generate_valid_response(
            llm,
            prompt
        )
    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence
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
        "When will I receive my refund?"
        #"How much does Zepto Pass cost?"
    )
    # Examples of querys :
    print("\nIntent:")
    print(result["intent"])
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    print(result["sources"])
    print("\nConfidence:")
    print(result["confidence"])