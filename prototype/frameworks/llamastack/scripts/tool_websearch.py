from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from termcolor import cprint
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access the environment variables
inference_model = os.getenv("INFERENCE_MODEL")
llama_stack_port = os.getenv("LLAMA_STACK_PORT")
ollama_url = os.getenv("OLLAMA_URL")
TAVILY_SEARCH_API_KEY = os.environ["TAVILY_SEARCH_API_KEY"]

print(f"Model: {inference_model}")
print(f"Llama Stack Port: {llama_stack_port}")
print(f"Ollama URL: {ollama_url}")

def create_http_client():
    from llama_stack_client import LlamaStackClient

    return LlamaStackClient(
        base_url=f"http://localhost:{llama_stack_port}", # return LlamaStackClient(base_url="http://localhost:8321", timeout = 6000)
        provider_data = {"tavily_search_api_key": os.environ['TAVILY_SEARCH_API_KEY']}  # according to https://llama-stack.readthedocs.io/en/latest/building_applications/tools.html
    )

# Initialize the Llama Stack client, choosing between library or HTTP client
client = create_http_client()  

# Register Search tool group
# according to https://llama-stack.readthedocs.io/en/latest/building_applications/tools.html
client.toolgroups.register( 
    toolgroup_id="builtin::websearch",
    provider_id="tavily-search",
    args={"max_results": 5},
)

print(client.toolgroups.list())

# Below is modified from websearch example from https://colab.research.google.com/github/meta-llama/llama-stack/blob/main/docs/getting_started.ipynb
agent_config = AgentConfig(
    model=os.getenv("INFERENCE_MODEL"),
    instructions="You are a helpful web search assistant, you can use websearch tool for unknown queries.",
    toolgroups=["builtin::websearch"],
    input_shields=[],
    output_shields=[],
    enable_session_persistence=False,
)
agent = Agent(client, agent_config)
user_prompts = [
    "Hello",
    "Which teams played in the NBA western conference finals of 2024",
]

session_id = agent.create_session("test-session")
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
    )
    for log in EventLogger().log(response):
        log.print()