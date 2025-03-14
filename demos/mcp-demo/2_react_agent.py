# Code bellow written following examples here: https://llama-stack.readthedocs.io/en/latest/building_applications
# Code bellow written following examples here: https://github.com/meta-llama/llama-stack-apps/blob/main/examples/agents/react_agent.py

from llama_stack_client.lib.agents.react.agent import ReActAgent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.types.shared_params.url import URL
from llama_stack_client import LlamaStackClient
from termcolor import cprint
import argparse
import logging
import os
from dotenv import load_dotenv

from client_tool import torchtune

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--remote", help="Uses the remote_url", action="store_true")
parser.add_argument("-s", "--session-info-on-exit", help="Prints agent session info on exit", action="store_true")
parser.add_argument("-a", "--auto", help="Automatically runs examples, and does not start a chat session", action="store_true")
args = parser.parse_args()

model="meta-llama/Llama-3.2-3B-Instruct"

# Connect to a llama stack server
if args.remote:
    base_url = os.getenv("REMOTE_BASE_URL")
    mcp_url = os.getenv("REMOTE_MCP_URL")
else:
    base_url="http://localhost:8321"
    mcp_url="http://host.containers.internal:8000/sse"

client = LlamaStackClient(base_url=base_url)
logger.info(f"Connected to Llama Stack server @ {base_url} \n")


agent = ReActAgent(
    client,
    model,
    builtin_toolgroups=["mcp::custom_tool"],
    json_response_format=True,
)

session_id = agent.create_session("react_session")

response = agent.create_turn(
    messages=[
        {
            "role": "user",
            "content": "I need to come up with a random number between 0 and 100 and the see if its considered `approved`. Once I know if its approved or not I need to write a nice 2 sentence response to the user telling them their results.",
        }
    ],
    session_id=session_id,
    stream=True,
)
for log in EventLogger().log(response):
    log.print()

