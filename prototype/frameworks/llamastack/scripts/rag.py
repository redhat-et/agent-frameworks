import os
from pathlib import Path
from termcolor import cprint
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent
from llama_stack_client import AgentEventLogger
from llama_stack_client import RAGDocument

load_dotenv()

# Configuration
LLAMA_STACK_PORT = os.getenv("LLAMA_STACK_PORT")
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")

def create_http_client():
    """Creates an HTTP client for communicating with the Llama Stack server."""
    endpoint = os.getenv("LLAMA_STACK_ENDPOINT")
    base_url = endpoint if endpoint else f"http://localhost:{LLAMA_STACK_PORT}"
    return LlamaStackClient(
        base_url=base_url
    )

def create_library_client(template="ollama"):
    from llama_stack import LlamaStackAsLibraryClient
    client = LlamaStackAsLibraryClient(template)
    client.initialize()
    return client

client = create_http_client()  # or create_http_client() depending on the environment

# there are few documents in the `llamastack/documents` folder, make sure to update the file path below with your local directory path
FILE_PATHS = ["<your local path for the repo dir>/documents/cake.rst", 
              "<your local path for the repo dir>/documents/car.rst", 
              "<your local path for the repo dir>/documents/house.rst", 
              "<your local path for the repo dir>/documents/technology.rst"]

documents = [
    RAGDocument(
        document_id=f"num-{i}",
        content=Path(file_path).read_text(encoding="utf-8"),
        mime_type="text/plain",
        metadata={},
    )
    for i, file_path in enumerate(FILE_PATHS) if Path(file_path).exists()
]
# Print warnings for missing files
missing_files = [file for file in FILE_PATHS if not Path(file).exists()]
if missing_files:
    print(f"Warning: {', '.join(missing_files)} not found. Skipping...")

# Register a vector db
vector_db_id = "my_documents"
response = client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    provider_id="faiss",
)

client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

# Create agent with memory
agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions="You are a highly reliable, concise, and precise assistant. "
        "When answering user queries, adhere to the following guidelines:\n"
        "1. **Strict Context Usage**: Base your response exclusively on the provided retrieved context.\n"
        "2. **Clarity and Brevity**: Provide clear, focused, and concise responses.\n"
        "3. **Handling Insufficient Information**: If the context lacks sufficient details, state that the necessary information is unavailable.\n"
        "4. **Avoid Inference or Speculation**: Stick to explicit context without speculation.\n"
        "5. **Disambiguation**: If a query is ambiguous, seek clarification before responding.\n"
        "6. **Neutral Tone**: Maintain objectivity in your responses.\n"
        "7. **User-Centric**: Ensure accessibility and clarity for a general audience.\n",
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {
                "vector_db_ids": [vector_db_id],
                "top_k": 3
            },
        }
    ],
)
session_id = agent.create_session("rag_session")
user_prompts = ["Give me a recipe to make a cake step by step?", "What are the advantages of electric vehicles?"]
# Ask questions about documents in the vector db, and the agent will query the db to answer the question.
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )

    for log in AgentEventLogger().log(response):
        log.print()

# Unregister all vector databases
for vector_db_id in client.vector_dbs.list():
    print(f"Unregistering vector database: {vector_db_id.identifier}")
    client.vector_dbs.unregister(vector_db_id=vector_db_id.identifier)